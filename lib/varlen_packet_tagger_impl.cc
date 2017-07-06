/* -*- c++ -*- */
/* TODO: add copyright info
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <cstdio>
#include <iostream>
#include "varlen_packet_tagger_impl.h"

extern "C" {
#include <fec.h>
#include "golay24.h"
}

namespace gr {
  namespace satellites {

#define VERBOSE 0

    varlen_packet_tagger::sptr
    varlen_packet_tagger::make(const std::string &sync_key,
                               const std::string &packet_key,
                               int length_field_size,
                               int max_packet_size,
                               endianness_t endianness,
                               bool use_golay, bool verbose)
    {
      return gnuradio::get_initial_sptr
        (new varlen_packet_tagger_impl(sync_key,
                                        packet_key,
                                        length_field_size,
                                        max_packet_size,
                                        endianness,
                                        use_golay, verbose));
    }

    varlen_packet_tagger_impl::varlen_packet_tagger_impl(
        const std::string &sync_key,
        const std::string &packet_key,
        int length_field_size,
        int max_packet_size,
        endianness_t endianness,
        bool use_golay,
        bool verbose) : gr::block("varlen_packet_tagger",
                        io_signature::make(1, 1, sizeof(char)),
                        io_signature::make(1, 1, sizeof(char))),
      d_header_length(length_field_size),
      d_mtu(max_packet_size),
      d_endianness(endianness),
      d_use_golay(use_golay),
      d_have_sync(false),
      d_verbose(verbose)
    {
      d_sync_tag = pmt::string_to_symbol(sync_key);
      d_packet_tag = pmt::string_to_symbol(packet_key);

      set_tag_propagation_policy(TPP_DONT);

      if (d_verbose) {
        std::cerr << alias() << "Header Bit Size: " << d_header_length << " MTU: " << d_mtu << std::endl;
      }
    }


    varlen_packet_tagger_impl::~varlen_packet_tagger_impl()
    {
    }

    int
    varlen_packet_tagger_impl::bits2len(const unsigned char *in)
    {
      // extract the packet length from the header
      int ret = 0;
      if (d_endianness == GR_MSB_FIRST) {
        for (int i=0; i<d_header_length; i++) {
          ret = (ret<<0x01)+in[i];
        }
      } else {
        for (int i=d_header_length-1; i>=0; i--) {
          ret = (ret<<0x01)+in[i];
        }
      }
      return ret;
    }

    int
    varlen_packet_tagger_impl::general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];
      int packet_len = 0;
      std::vector<tag_t> tags;

      register uint32_t golay_field;
      int golay_res;

      if (d_have_sync) {
        if (d_header_length > ninput_items[0])
          return 0; // not enough data yet
        
        if (d_use_golay) {
          d_header_length = 24; // always 24 bits long (12 is length)
          golay_field = bits2len(in); // copy bits
          if (d_verbose) {
            d_header_length = 12; // for debugging
            packet_len = 8 * bits2len(&in[12]);
            d_header_length = 24; // always 24 bits long (12 is length)
            std::cerr << "Varlen packet decoder" << std::endl;
            std::cerr << "\tHeader:     " << boost::format("0x%06x\n") % (0xFFFFFF & golay_field);
            std::cerr << "\tRaw Length: " << std::dec << packet_len << std::endl;
          }
          golay_res = decode_golay24(&golay_field);
          if (golay_res >= 0) {
            if (d_verbose) {
              std::cerr << "\tGolay decode successful." << std::endl;
              std::cerr << "\tErrors:     " << std::hex << golay_res << std::endl;
              std::cerr << "\tCorrected:  " << boost::format("0x%06x\n") % (0xFFFFFF & golay_field);
              std::cerr << "\tLength:     " << std::dec << 8 * (0xFFF & golay_field) << std::endl;
            }
            packet_len = 8 * (0xFFF & golay_field);

          } else {
            if (d_verbose) {
             std::cerr << "\tGolay failed: " << std::hex << golay_res << std::endl;
            }
          }          

        } else { 
          packet_len = 8 * bits2len(in);
        }

        if (packet_len > d_mtu) {
          //std::cerr << "Packet too large!" << d_mtu << std::endl;
          d_have_sync = false;
          consume_each(1); // skip ahead
          return 0;
        }
        
        if ((ninput_items[0] >= packet_len + d_header_length) &&
            (noutput_items >= packet_len)) {

          memcpy(out, &in[d_header_length], packet_len);
          //std::cerr << "Adding tag " << packet_len << " offset " << nitems_written(0);
          add_item_tag(0, nitems_written(0),
                       d_packet_tag,
                       pmt::from_long(packet_len),
                       alias_pmt());
          d_have_sync = false;
          consume_each(d_header_length);
          // consume the packet too?
          // ... not consuming everything allows for multiple syncs per 'packet'
          return packet_len;
        } /*else {
          std::cerr << "we have data to send!";
          std::cerr << "pl: " << packet_len << " input-items " << ninput_items[0] << std::endl;
          std::cerr << "outputs: " << noutput_items << std::endl;
        }*/

      } else {
        // find the next sync tag, drop all other data
        get_tags_in_range(tags, 0, nitems_read(0),
                          nitems_read(0) + ninput_items[0],
                          d_sync_tag);
        if (tags.size() > 0) {
          d_have_sync = true;
          consume_each( tags[0].offset - nitems_read(0) );
        } else {
          consume_each(ninput_items[0]);
        }
        return 0;
      }
    }

  } /* namespace satellites */
} /* namespace gr */

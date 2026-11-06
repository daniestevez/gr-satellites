# Security Policy

These days it is far too easy to find bugs in most open source applications by
using AI. One of the strengths of open source rests on the fact that everyone
can contribute improvements to make the software better. Lately, gr-satellites
is seeing an increase in security vulnerability reports written by people using
AI to find bugs and claim CVEs. It does not seem that these people want to
contribute to make the software better. It seems that they only want to obtain
CVEs with little effort from their side. This situation has led to the following
security policy.

Security vulnerabilities should be reported through
[GitHub security advisories](https://github.com/daniestevez/gr-satellites/security/advisories/new).
Regular bugs which do not constitute a security vulnerability should be reported
as [GitHub issues](https://github.com/daniestevez/gr-satellites/issues).

Security vulnerabilities and bug reports should follow the [LLM Usage
Policy](https://github.com/daniestevez/gr-satellites/blob/main/LLM_POLICY.md).
Among other things, this policy implies that LLMs can be used to discover bugs
and security issues, but the report and any proofs of concept or supporting
material need to be written from scratch by hand by a person. For reports that
do not follow the LLM policy, the gr-satellites maintainers will act as they
deem appropriate (for instance by fixing the issue that is reported). A response
to the non-compliant report will not be given other than to state that it does
not follow the policy.

Because of the nature of gr-satellites, a valid security vulnerability proof of
concept must use the attack surface that is available and cause a security
issue. The attack surface is, generally speaking, limited to inputs of the
gr_satellites command line tool (IQ input) and configuration files and other
environment. Memory issues are a mechanism through which a security issue could
be caused, but they do not constitute a security issue on their own. The proof
of concept cannot be limited to showing that there are invalid memory accesses.

Some gr-satellites blocks have API contracts that state that inputs should have
a certain size or format. In some cases these contracts are only implicit in the
implementation rather than documented explicitly. While it is desirable to have
robust implementations that handle gracefully inputs that do not comply with the
contract, and it is also desirable to have all these contracts spelled out in
documentation, as long as all users of a given block within gr-satellites comply
with the API contract, the potential consequences of breakage of the API
contract cannot constitute a security issue. In particular, a custom flowgraph
that (mis)uses a block in a way in which it is not used in gr-satellites in
order to cause a security issue is not a valid proof of concept, since the
attack surface for gr-satellites does not include an attacker making custom
flowgraphs (these are arbitrary C++ or Python code and can literally do
anything).

# Leads

Format per lead:
### L-NNN · STATUS · short title
- **Where:** target, folder/cote, page
- **Verbatim:** "<transcription in original language>"
- **Plain English:** <gloss>
- **Why it might matter:** <one or two sentences, clearly marked as interpretation>
- **Novelty check:** <queries run, what was found, with links>
- **Next:** <what would move it forward>

## Unverified candidates (label: self-checked; awaiting review)

_New proposals go here: one line each — `L-NNN · self-checked · title · candidates/L-NNN.md`. A reviewer moves the entry down after writing a verdict._

_Reviewed leads (all four checks done, independent unanchored reviews written up): `candidates/L-019.md` (Riemann shock relations / Prandtl–Meyer, 7/10 if hand & date), `candidates/L-032.md` (Riemann free-plate frequency equation, 6–7/10 if hand & date). Expert verdicts welcome via the issue template._

## Active leads (passed rule 9 with stated caveats)

### L-032 · PASSED ALL 4 CHECKS · 6-7/10 IF Riemann's hand & pre-1866 (independent check: 6; literature check: 7) · Riemann c.1856-63: exact 3-D frequency equation for flexural vibrations of a free elastic plate = antisymmetric Rayleigh-Lamb equation (Rayleigh 1889)
- **Where:** SUB Göttingen, Cod. Ms. B. Riemann 26 ("Mathematische Notizen", 1853-1863; the same bundle as L-019), fol. 228r = transcript c446, image 00000447 (gdz:DE-611-HS-3206190). Pencil. Found by the Göttingen gap-fill 2026-11-09 (deep read surprise 6; the page had no deep read before because the first run's JSON failed to parse).
- **Verbatim (read on the scan by a maintainer 2026-11-09):** "p = sin σz λ; u = sin σz ∂λ/∂x + sin τz aτ ∂λ/∂x; v = (same) ∂λ/∂y; w = cos σz σλ − cos τz aϱλ; (−σ² − ϱθ − σ²θ) sin σc + aτϱ sin τc = 0; cos σc 2σ + cos τc a(τ² − ϱ) = 0; τ'+σ' = λ, τ'−σ' = 1/λ; 1/(1+2θ) − σ'² = 2(1+θ)/(1+2θ) − τ'² = ϱ'; sin τc cos σc / (sin σc cos τc) = (τ'² − ϱ')[σ'²(1+θ) − ϱ'θ]/(2σ'τ'ϱ')" then rational forms in λ² + λ⁻² and 1/r². Lower third unrelated (linear displacement field, rotation operators).
- **Plain English:** Riemann takes an infinite elastic plate of thickness 2c, writes the exact 3-D displacement for the bending (antisymmetric) modes as a dilatational part plus a shear part, imposes zero stress on both faces, and eliminates the amplitude ratio to get the transcendental equation that fixes frequency against wavelength — the "Rayleigh-Lamb frequency equation" for Lamb waves, in the standard literature first published by Lord Rayleigh (Proc. LMS 20, 1889) with Lamb (1889) conceding priority to him; Love's Treatise names no one earlier. θ is Kirchhoff's 1850 ratio λ_Lamé/(2μ), so the sheet is post-1850; Riemann announced lecture courses on "Elastizität fester Körper" SS 1856 and WS 1859/60 (Nachträge p. 114), modelled on Lamé (letter 7 July 1857).
- **Step 2 (code):** targets/riemann/verify/r26_228r_plate_flexural.py — with Δ₂λ = −ϱλ: σ_zz/(2μλ) at z=c equals the page's first equation exactly and σ_xz/(μλ_x) equals the second exactly (θ = λ_L/2μ); eliminating a gives tan τc / tan σc = −(τ²−ϱ)(σ²(1+θ)+ϱθ)/(2στϱ), which with k_T²/k_L² = 2(1+θ) is identically the antisymmetric Rayleigh-Lamb equation tan(qh)/tan(ph) = −(k²−q²)²/(4k²pq). The page's written ratio differs by an overall sign and the sign of the ϱ'θ term (a slip in the working, or a reading error in pencil); the two boundary equations above it are correct.
- **Step 3 (literature, agent 2026-11-09, sources read):** Rayleigh 1889 (Sci. Papers III no. 156) claims the method is new and "not limited to small thickness", cites no earlier exact plate solution; Lamb 1889 Appendix: "the propagation of waves in an infinite plate has been fully treated by Lord Rayleigh"; Love 1920 Art. 333-334 credits Rayleigh only. Poisson 1829 / Cauchy 1828: series in the thickness, not exact. Lamé 1852 13e Leçon: modes with shear-free faces only (normal traction left free; criticised by Todhunter-Pearson), no frequency equation. Kirchhoff 1850/1876, Clebsch 1862, Saint-Venant 1883: thin-plate theory only. Riemann's Werke, Hattendorff's PDG lectures (1869), Riemann-Weber (1900): no plate vibrations; Nachträge 1902 report on Akt 26 mentions no elasticity. NOT accessed: Lamb 1917 intro; Mindlin 1960; Graff.
- **Dating / hand:** undated leaf inside fol. 212-233 (loose calculations), nearest dated leaf fol. 183v (1853) before it, bundle dated 1853-63; Kirchhoff θ ⇒ after 1850; elasticity courses 1856, 1859/60. Hand not yet confirmed by a palaeographer (same caveat as L-019; same bundle).
- **Provisional rating:** 7/10 if the hand is Riemann's and the leaf pre-1866 (agent step 3 also says 7). Reasons against: unpublished working sheet with a sign slip and no follow-up; the problem is a natural exercise after Lamé's lectures. Reason for: the exact traction-free frequency equation for a plate is dated 1889 by everyone, including Lamb and Love.
- **Step 4 (unanchored check, fresh agent given scan + transcription + date bracket only, 2026-11-09):** identified the page independently as the antisymmetric Rayleigh-Lamb problem; confirmed by sympy that the ansatz satisfies the Navier equations and both free-face conditions match the page exactly; found TWO sign slips in the written ratio (sign of ϱ'θ and overall sign) and showed the page's final rational form is faithful to the slipped version (so the last lines are wrong as written); r is Poisson's ratio in disguise (1/r² = 1−ν); first publication Rayleigh, read 11 April 1889 (Proc. LMS 20, eq. 47), Lamb 1889 conceding, Love crediting Rayleigh; Poisson/Cauchy series, Lamé 1852 special modes only, Clebsch thin plates; attribution to Riemann "not found" in Hattendorff 1869, Riemann-Weber 1900/1910, Todhunter-Pearson, Love, Papadopoulos 2017, Kalliope. Rating 6/10: "the obvious next step beyond Lamé, done privately and left unfinished", vs. a 30-year anticipation of a result everyone dates to 1889. Neighbour 227r may be thin-plate (biharmonic) work — unverified.
- **Verdict:** 6-7/10 conditional on hand and date (same two questions as L-019; same bundle). Not usable today; a clean historical anticipation if confirmed. EV below L-019 because of the sign slips and no follow-up.
- **Blind handwriting test (2026-11-09, fresh agent, nine pages under random letters, key withheld):** target = fol. 228r; controls = Riemann dated leaves (letter to his brother Quickborn 1853 = G, pencil slip 24 Sept 1858 = A, letter draft 5 Oct 1861 = B), the L-019 sheet fol. 70v = F, Weierstraß (Cod. Ms. 19 fol. 101r, 103r = E, D), H. Weber (fol. 116r, 118r = J, I). Result: target matched to F (the L-019 shock sheet) at 65-70% on stroke construction (∂ as small closed loop + right hook, ϱ tail, long-s in ſin/coſ/conſt, ꝛ-like r, two-stroke x, hooked y, flat 2); both separated from Weierstraß (D/E grouped together at 70%, ≠ C/F at ~65%). Weak points, stated by the agent: the maths pages carry no German prose, so C/F could not be anchored to Riemann's letter hands (A only 45%); and it grouped Riemann's 1861 letter draft (B) with Weber's pages (I/J) at 60-65% — a miss that shows the method's limit for prose vs. notation. Net: supports "same writer as L-019", does not independently establish Riemann; the palaeographer remains the decisive step for both sheets.
- **Writer-identification classifier (2026-11-09; see L-019 for method and accuracy):** fol. 228r → Riemann 0.971 (histogram variant) / 0.809 (VLAD variant, Gauss 0.18) — the least certain of the four targets, still Riemann in both; nearest training pages are Riemann pages from both volumes.
- **Next:** add fol. 228r to the L-019 expert request (same bundle, same questions: hand, paper, ink/pencil, neighbouring leaves).

### L-031 · DUPLICATE (published by the editors: Riemann, Werke, Nachträge 1902, IV. Mathematische Noten, Note D, pp. 99-100, with "Cf. Picard 1885") · Riemann c.1862-65: closed 1-forms on an algebraic surface
- **Where:** SUB Göttingen, Cod. Ms. B. Riemann 19 (R.AbelTheta), fol. 97r-97v = transcripts c196-c197, images 00000197-198 (gdz:DE-611-HS-3206670). Found by the Göttingen gap-fill 2026-11-09 (deep read surprise 5 on both pages; pages had no deep read before because the first run's JSON failed to parse).
- **Verbatim (97r, read on the scan by a maintainer 2026-11-09):** "ξ ∂f/∂x + η ∂f/∂y + ζ ∂f/∂z = f·φ(x,y,z)" with multidegree labels f:(m,n,r), ξ:(m−1,n−2,r−2); "∂ξ/∂x + ∂η/∂y + ∂ζ/∂z − ϱ = 0"; "f(x,y,z)=0"; "(−η dx + ξ dy)/(∂f/∂z) vollständiges Differential = (η dz − ζ dy)/(∂f/∂x) = (ζ dx − ξ dz)/(∂f/∂y)"; "(2m−1)(2n−1)(2r−1) Bedingungen"; "Constanten 4mnr+4"; then a homogeneous version in x,y,z,t ("t(ξf_x+ηf_y+ζf_z+τf_t)=0"). 97v: the same in index form with an antisymmetric a_{ι,ι'}: f_{ι''}a_{ι,ι'}+f_ι a_{ι',ι''}+f_{ι'}a_{ι'',ι} = f·b_{ι,ι',ι''}, b = cyclic sum of ∂a/∂x; then a linear substitution to a surface of degree n in four homogeneous variables. The top of 97r is unrelated (hyperelliptic theta quotient vs branch points).
- **Plain English:** Riemann asks when a rational 1-form on an algebraic surface, written via a polynomial vector field (ξ,η,ζ) tangent to the surface, is closed ("a complete differential"), finds the criterion div(ξ,η,ζ) = ϱ on the surface (where V·∇f = fϱ), and starts counting free constants against conditions for surfaces of multidegree (m,n,r) and for a surface of degree n in P^3. Interpretation: this is the beginning of the theory of integrals of total differentials on surfaces (Picard 1884-85; irregularity q), ~20 years before Picard; the dimension count points toward "generic surfaces have none".
- **Step 2 (code):** targets/riemann/verify/r19_97r_total_differentials.py — with generic polynomial data, the three expressions agree on f=0 given tangency, and the form is closed on f=0 iff div V = ϱ (identity via the residue of (ι_V vol)/f: dω = (div V − ϱ) dx∧dy/f_z); a perturbed tangent field with div ≠ ϱ is not closed. Riemann's criterion is correct.
- **Step 3 (literature):** DONE — see verdict — Werke/Nachträge contents; Picard-Simart; Bardelli on origins of irregularity; Neuenschwander on Cod. Ms. 19. Provisional: not in the 1876/1892 Werke to my knowledge; Picard–Simart credit Clebsch/Noether for surface genus, nobody for Riemann on total differentials.
- **Step 4 (unanchored):** stopped as moot after step 3.
- **Why it might matter (interpretation):** if no printed source has it, it is a clean "finished-but-uncredited" anticipation at the level of a historical note (likely 5-6); it would reach 7 only if the count on the page is a correct statement that smooth surfaces in P^3 carry no closed 1-forms of the first kind (Noether/Picard), which needs a careful reading of the arithmetic on the page.
- **Next:** literature + unanchored verdicts; then read 97v arithmetic line by line; dating within Cod. Ms. 19 (neighbouring dated sheets).

- **VERDICT 2026-11-09 — DUPLICATE, failure mode 3 (editors already published it).** Max Noether printed a formula-level summary of exactly this sheet in the Nachträge (1902), IV "Mathematische Noten (ausgezogen aus dem Nachlaß)", D: "Integrale einfacher totaler Differentialien, erster Gattung, bezüglich einer algebraischen Fläche", pp. 99-100, source line "Akt Nr. 19, Konv. 19β, d); Nr. 26, Bogen 1": the three expressions for du, the identity ξF_x+ηF_y+ζF_z = F·φ with φ = div(ξ,η,ζ), the homogeneous form, "Versuche der Konstantenzählung", the n-variable generalisation, and an irregular example (symmetric square of a genus-2 curve, Nr. 26 Bogen 1), ending "(Cf. Picard in Journ. de Math., sér. IV, t. 1, 1885.) N." Verified on the OCR of the 1902 printing (archive.org bernhardriemann01riemgoog, Nachträge p. 100). Picard published the same criterion independently in 1884-85 and drew the non-existence conclusion for general surfaces; Noether (1887) claimed private knowledge since 1868.
- **What is still true and small:** the folio-level identification (Cod. Ms. B. Riemann 19, fol. 97r-v = "Konv. 19β d", the "Italien – ϑ-Functionen" convolute, dated leaves Göttingen Oct 1862 – Pisa Jan 1865) and the fact that the later historiography of irregularity (Houzel 1991, Kleiman 2005/2014, Ciliberto, Picard-Simart II) does not mention Noether's note. Rating 3/10 as a historical footnote. Unchecked: Bardelli 1994 (Palermo Suppl. 36), Bottazzini-Gray, Laugwitz.
- **Lesson (again):** the editors' reports on the same folder kill candidates; check the Nachträge "Mathematische Noten" and "Berichte über die Akten" before any Riemann Nachlass claim. The hot-list entry for this page is closed.

### L-030 · CHECKED (all 4 steps; FROZEN) · Grothendieck 1953 functional-analysis folder: five clusters, best 6/10
- Independent check (2026-11-08), reviewer read exposé 91 (1954), exposé 113 (1955) and the 1956 Fredholm paper directly:
  A multiplier algebra (pp.3-4): 5 - unpublished, uncredited (Busby 1968 / Akemann-Pedersen-Tomiyama 1973 form), but an
    elementary consequence of C'' being a von Neumann algebra (Sherman-Takeda), which he invokes as known.
  B p-subadditivity p < 1 (pp.75, 128-129): 3 - IN PRINT: exposé 113 §6 (lemma + S_p consequence); under-credited outside
    the vN literature (McCarthy/Rotfel'd 1967 get the credit) but that is the published text's story, not the archive's.
  C trace formula (pp.78-79, struck): 5 - the claim is in exposé 91 (1954) §4c without proof ("det(1+zu) est fonction
    entière de genre 0 = Π(1+zλ_i)"), Lidskii 1959 proved it; these pages show exactly where his proof stopped (Robert
    2017 / Pisier 1988 noted he "did not pursue the argument to the end").
  D Seiler-Simon inequality (pp.123-125): 6 - the inequality det(1+|A+B|) ≤ det(1+|A|)det(1+|B|) (and the partial-product
    form) is ASSERTED in exposé 113 §6 for B(H) with a one-line method; Fack, J. Funct. Anal. 50 (1983) "Proof of the
    conjecture of A. Grothendieck on the Fuglede-Kadison determinant" and Fack-Kosaki 1986 ("the Grothendieck
    inequality") credit him in the vN community; Seiler-Simon 1975 ("appears to be new") and the trace-ideal literature
    do not. The archive adds the full proof (same route as Seiler-Simon) and the sharper Corollaires 2-3 (mixed
    Cauchy-Schwarz for exterior powers, not found anywhere). A naming split between two communities, not a missed result.
  E Powers-Størmer-type conjecture (p.145): 3 - hedged guess on a poorly legible page; not in print; BKS 1975 / Ando 1988.
  => nothing at 7. FROZEN. (The maintainer's rule-9 amendment half-applies to D: statement public since 1955, recognised by
  Fack 1983; only the proof and the sharper lemma are new.)
- (old header) UNVERIFIED CANDIDATE · Grothendieck 1953: the multiplier algebra of a C*-algebra via the bidual
- Source: grothendieck.umontpellier.fr 1.pdf "Analyse fonctionnelle : notes manuscrites (s.d.), lettre (1953)" (149 pp,
  1953), pp.3-4 (deep surprise 5, 5).
- Content (p.3, read by me, matches): C a C*-algebra; continuous linear endomorphisms T commuting with translations
  x → xy; T'' is a weakly continuous endomorphism of C'' commuting with x → xy for y ∈ C hence for all y ∈ C'';
  "Donc de la forme x → ux (u ∈ C'')"; Γ_g = {u ∈ C'': uC ⊂ C} ≅ the algebra of such endomorphisms (normed-algebra
  isomorphism); T hermitian/positive ⇔ x*T(x) hermitian/≥ 0; "Soit Γ l'ensemble des u ∈ C'' tels que uC ⊂ C, Cu ⊂ C.
  C'est une sous-C*-algèbre involutive"; for C ⊂ R, Γ_1 = idealizer of C in R, φ: Γ_1 → Γ a *-representation; (p.4 per
  reader) φ(a) = weak-lim ax along an approximate unit; if R is a von Neumann algebra with C weakly dense, Γ ≅ Γ_1.
- Modern reading (interpretation): the multiplier algebra M(C) realised as the idealizer of C in its enveloping von
  Neumann algebra C'', with left centralizers = left multiplications by elements of C'' - usually credited to Busby 1968
  (double centralizers), Johnson 1964 (centralizers), Akemann-Pedersen-Tomiyama 1973 / Pedersen 1979 §3.12 (bidual
  form). Uses C'' as a W*-algebra (Sherman 1950 / Takeda 1954) in 1953.
- Caveats: Grothendieck's published 1957 "Un résultat sur le dual d'une C*-algèbre" uses the bidual; check whether it
  or his 1955 Memoir / Résumé contain this; Wendel 1952 (L¹(G) multipliers) is prior art for the idea. CAVEAT: cote 1
  p.2 = table of contents "No 1 Réarrangements de fonctions ... No 4 Mesures spectrales, réarrangement décroissant d'un
  opérateur ... No 6 L'inégalité fondamentale AB dans les anneaux d'opérateurs" = the plan of Grothendieck's PUBLISHED
  Séminaire Bourbaki exposé 113 (1955) "Réarrangements de fonctions et inégalités de convexité dans les algèbres de von
  Neumann" -> much of the folder is a draft of a published text; check whether the multiplier pages are in it.
  Also p.75 [5]: p-subadditivity Σ s_i(u+v)^p ≤ Σ s_i(u)^p + Σ s_i(v)^p (0 < p < 1), for every partial sum, via a
  multiplicative Weyl/Horn inequality for Π(1 + r s_i) integrated against a decreasing φ (Rotfel'd's route, credited
  1967-76; Thompson); explicit question: which f make Σ_{i≤n} f(s_i) subadditive. Part of the rearrangements series ->
  compare with Bourbaki exposé 113 (1955).
  Also p.78 [5] (struck through): det(1+zu) = Π(1+zλ_i) and Tr u = Σλ_i for trace-class operators on Hilbert space
  (Lidskii 1959) via entire-function theory; decisive step asserted. Memory (to verify): Grothendieck's published
  "La théorie de Fredholm" (Bull. SMF 1956) contains this trace formula (Hilbert / 2/3-nuclear case) -> likely a draft
  of published work.
  Also pp.123-124 [5]: det(1+|A+B|) ≤ det(1+|A|)det(1+|B|) and |det(1+A+B)| ≤ det(1+|A|)det(1+|B|) for trace-class
  A, B via a mixed Cauchy-Schwarz inequality for exterior powers ‖u_1∧…∧u_n‖_1² ≤ α_n(|u_i|)α_n(|u_i|') (credited
  Seiler-Simon 1975 / Rotfel'd). Same series. p.124 READ BY ME (deep [6], matches): "Corollaire 3 |det(1+A+B)| ≤ ½(det(1+
  |A|+|B|) + det(1+|A|'+|B|')); Corollaire 4 |det(1+A+B)| ≤ det(1+|A|)det(1+|B|)" with proof (reduce to h, k ≥ 0;
  det(1+h+k) = det(1+h)det(1+Hk), H = (1+h)^{-1}, ‖Λ^n H‖_∞ ≤ 1); "Corollaire 5 det(1+|A+B|) ≤ det(1+|A|)det(1+|B|)".
  = the Seiler-Simon inequality (PNAS 1975; Simon, Trace Ideals). KEY QUESTION for the check: is it in Grothendieck's
  "La théorie de Fredholm" (Bull. SMF 84, 1956) or Bourbaki exposé 113 (1955)? If not: named inequality anticipated
  by 22 years, uncredited (rule 9 amendment candidate).
  Also p.128-129 [5]: duality ‖A‖_p = sup |Tr AB| over ‖B‖_{p'} ≤ 1 (p ≥ 1); for 0 < p < 1 the subadditivity of S_p via
  x^p = (p sin πp/π) ∫ log(1+tx) t^{-1-p} dt combined with det(1+t|A+B|) ≤ det(1+t|A|)det(1+t|B|) - exactly the
  Seiler-Simon 1975 method (Simon, Trace Ideals); identity S_p(A) = c_p ∫ log M_{|A|}(r) r^{-1-p} dr.
  Also p.145 [5] (rough notes): conjectured inequality ‖|h|^r − |k|^r‖^{1/r} ≤ ‖h − k‖ (0 < r < 1) for the power map
  on positive operators in Schatten norms - contains the Powers-Størmer inequality (1970, r = 1/2, p = 1) and the
  Birman-Koplienko-Solomyak 1975 / Ando 1988 inequalities; conjecture only. Sent to the running check as cluster E.
  NEXT: combined independent check for the 1953 folder (RUNNING).

### L-029 · CHECKED 5/10 (all 4 steps; FROZEN) · Grothendieck 1965-77: "absolute cohomology" guesses for Tate motives over F_q and Spec Z (Weil-étale-type values)
- Independent check (2026-11-08): 5/10. H¹(F_q, Z(n)) = Z/(q^n−1) = Quillen 1972 (no p-torsion); H⁰ = H¹ = Z for Z over F_q
  = Lichtenbaum 2005 / Geisser 2004 Weil-étale values; Spec Z: Z in degree 0 and Z(1) in degree 3 = Lichtenbaum 2009
  Thm 5.10 + Flach-Morin duality, correct modulo 2-torsion (Z/2 = Z^× missing); "n ≠ 0" iso false for n = 1, self-
  corrected on p.173 to n ≠ 1 (consistent with Borel 1974). No source credits Grothendieck for Weil-étale-type values
  (Geisser, Flach-Morin, Morin all start from Lichtenbaum). Consistency guesses from ℓ-adic + Artin-Verdier; no
  definition, no zeta link. FROZEN.
- Source: cote 15, p.171 cover "Calculs de cohomologie absolue des Motifs de Tate Z(i)", p.172 (deep [5]), p.173.
- Content (read by me, matches): ℓ-adic: H^1(π, Z_ℓ(n)) ≅ Z_ℓ/(1−q^n); then "absolute" (motivic, double-struck H):
  H^i(F_q, Q(n)) = 0 for n ≠ 0; H^0(F_q, Q) = H^1(F_q, Q) = Q; H^0(F_q, Z) = Z, H^1(F_q, Z) = Z "(mod p-groupes?)";
  H^1(F_q, Z(n)) = Z/(1−q^n) (n ≠ 0); H^i(Spec Z, Z(1)) = Z for i = 3, 0 otherwise; H^i(Spec Z, Z) = Z for i = 0, 0
  otherwise; H^i(Spec Z, Q(n)) ≅ H^i(U, Q(n)) for U Zariski-open, n ≠ 0. p.173: Gysin sequence for Spec Z ⊃ U with
  Q(n), "Si n ≠ 1: iso tout i [est-ce vrai ??]"; n = 1: H^i(X, Q(1)) = 0 except i = 3.
- Interpretation (unverified): H^1(F_q, Z) = Z is cohomology of the discrete Frobenius group (Weil group), the defining
  feature of Lichtenbaum's Weil-étale cohomology (2005); Z/(1−q^n) = K_{2n−1}(F_q) (Quillen 1972); "Spec Z as an integral
  homology 3-sphere with Z(1) dualising in degree 3" = integral form of Artin-Verdier (1964) / Mazur's 3-manifold
  analogy (1973, credited to Mumford). Caveats: date uncertain within 1965-77 (Quillen 1972, Borel 1974 are in that
  window; Borel's K_{4k+1}(Z)⊗Q = Q contradicts "H^i(Spec Z, Q(n)) ≅ H^i(U, Q(n))"-type vanishing unless he meant
  something else - he himself writes "est-ce vrai ??"); speculative page with question marks. NEXT: combined check.

### L-028 · CHECKED 5/10 (all 4 steps; FROZEN) · Grothendieck c.1965-77: motives over F_p as a gerbe classified in H²(Q,H), split at ℓ ≠ p, isocrystal torsor at p
- Independent check (2026-11-08): 5/10. Published item for item in Langlands-Rapoport 1987 §2-3 (local gerbes: trivial at
  ℓ ≠ p, real Weil-group/quaternion gerbe at ∞, Dieudonné gerbes at p; Hasse principle Lemma 3.5; slope cocharacter ν_2)
  and Milne 1994/2003/2006/2007; Milne 1994 abstract: "many of the results were known to Grothendieck, Langlands,
  Rapoport, and Deligne, but often not published" (undated). Pages may date 1965-77 (versos 1968-77). μ_2 factor not
  matched anywhere. Nothing usable now. FROZEN.
- Source: grothendieck.umontpellier.fr 15.pdf "Théorie arithmétique. Théorie de Galois des motifs (1965)" (227 pp,
  1965-c.1977), p.6 (deep surprise 5). Neighbouring pages = stray Lipman typescript (rational double points).
- Content (read by me, matches): motives over F_p "à isogénie près" with grading, augmentation, fibre functors T_ℓ and
  F_0, F_ℓ; "la connaissance de M, graduation, augmentation, F_0 est connue quand on connaît la classe de ℋ comme
  H-gerbe, i.e. un élément ξ_0 ∈ H²(Q,H) ≃ H²(Q,H°) × H²(Q,μ_2)"; grading ↔ i*: Γ → Z with i*(λ) = ν ⇔ |λ| = p^{ν/2}
  (Γ = characters of H = Weil numbers); for ℓ ≠ p the ℓ-adic F_ℓ splits the gerbe over Q_ℓ, so the data ⇔ ξ ∈ H²(Q mod
  T, H), T = ⊔_{ℓ≠p} Spec Q_ℓ, "ξ splitte sur les places finies ℓ ≠ p"; at ℓ = p the fibre functors T_p (on isocrystals)
  and F_p "diffèrent par une torsion sous (G/H)~_{Q_p}" with G/G° ≅ Ẑ, G°/H ≅ G_m.
- Modern reading (interpretation): the local-global structure of the Langlands-Rapoport pseudo-motivic gerbe (1987) /
  Milne "Motives over finite fields" (1994): class in H²(Q,P), P = Weil-number protorus, trivial at ℓ ≠ p, isocrystal
  torsor at p. Extra: explicit μ_2 factor (sign/commutativity constraint) left unresolved.
- also p.10 [5] (transcription, poor legibility): ξ determined by its finite local components ξ_ℓ (Hasse-principle
  argument); "M n'a pas de foncteur fibre sur R" (three sketched reasons incl. a rank-1 degree-1 representation of G°
  with Ext² obstruction, and a Hasse-Weil / elliptic-curve argument), hence ξ_∞ ≠ 0, tied to H²(Q_p, ·).
- also p.41 [5] (transcription, very hard to read): the supersingular ("Deuring") category modelled place by place
  (Tate modules at ℓ ≠ p, rank-2 slope-1/2 F-crystals at p, a real gerbe at ∞), comparison torsor under adelic square
  classes × Z/2, Frobenius action; conclusion not on the page.
- also p.51 [5]: the archimedean place: a canonical real gerbe G(ξ_p)_R for each class ξ_p; for the Deuring (super-
  singular) class it is non-trivial because End⁰ ⊗ R = Hamilton quaternions (no R-valued fibre functor); "situation
  pas encore très jolie"; asks for a description independent of elliptic curves.
- also p.120 [5]: for motives over F_q (assuming Tate), G° a pro-torus with character group M ⊂ Weil q-numbers in a CM
  field; a distinguished conjugacy class of cocharacters i: G_m,C → G_C, λ ↦ (1/n) v_𝔭(λ) (the slope/Newton cocharacter),
  with ī·i = j (weight) and ε∘i = id; question whether Aut(G°, ε, μ) acts transitively on polarisations.
- (related, cote 13 p.33 [5], 1965) "Situation abstraite des doubles réseaux": ⊗-category over k with fibre functors T
  (over k) and T' (over K) identified over L; data ⇔ (G = Aut⊗T, torsor P = Isom(T_K, T'), φ ∈ P(L)); doubly-rational
  classes = invariants of the group H generated by the Zariski closure of the comparison; full-faithfulness criterion
  V^H = V^G (epimorphic subgroup, not genericity). Same family as the period-torsor pages (L-027, checked 4/10).
  Also 13 p.47-48 [5] 'double visage': is the de Rham-Betti realisation (with comparison, without Hodge filtration)
  fully faithful? ⇔ V^G = V ∩ g(V_Q̄) for the period point g ∈ G(C)/G(Q̄); a weaker sufficient condition (the group
  generated by the comparison contains a Borel of G°). = the de Rham-Betti full-faithfulness question (Bost-Charles
  2016 territory). Same family, same verdict. Also 13 p.49 [5] (gap-fill): the period conjecture in Hom form (1965) and
  a families version via algebraic connections without filtration (cf. Ayoub's relative period conjecture). Same family.
  Also cote 8 p.64 [5] (c.1970, "Cristaux ... gribouillis"): the Hodge-Tate decomposition T_p(M)⊗C_p ≅ ⊕ T_Hdg^{i,j}⊗C_p(−i)
  read Tannakianly: a trivialisation C_p(1) ≅ C_p gives a point of the étale/Hodge comparison torsor P(C_p), hence a
  G_m-equivariant map V(Z_p(−1))* → P (Fontaine's B_HT formalism 1982 / Serre's HT cocharacter 1967 in substance);
  descent compatibility left open. Same family; noted only.
- Milne 2006 "Motives over F_p" (arXiv math/0607569) checked: no history of the H² class; cites LR 1987 / Milne 1994.
- Caveats: the band/Weil-number description is traceable to Grothendieck via Saavedra 1972; LR 1987 and Milne credit
  Grothendieck's ideas in general; expected to be a priority/history fact (~5) like L-024. NEXT: check Milne's history
  (arXiv math/0607569) for attribution of the H² class + local conditions; decide on full check by upside.

### L-027 · CHECKED 4/10 (all 4 steps; FROZEN; conjecture FALSE as written) · Grothendieck c.1969-72: "Conjecture de transcendance forte" for periods + Hodge decomposition
- Independent check (2026-11-08): 4/10. The boxed statement trdeg k(α,β)/k = g + u is FALSE for motives over real fields:
  complex conjugation acts on Betti cohomology by F∞ with C̄ = F∞·C (Deligne 1979; Brown, Notes on motivic periods §3.6),
  so the Hodge decomposition β is rational in the periods α, k(α,β) = k(α), trdeg ≤ g. Elliptic check: non-CM curve over
  Q predicts 5 but has only 4 periods with β rational in them (numerically verified by the reviewer on y² = 4x³ − 4x − 1);
  "τ, τ̄ independent" fails for every Q̄-curve isogenous to its conjugate. Corrected form = ordinary period conjecture for
  M ⊕ M̄ (Brown's single-valued period matrix s = C̄^{-1}C is exactly the β-datum) - nothing new. Strong form: not found
  in André 2009, Ayoub 2014 (who "saw it in Grothendieck's manuscripts in Montpellier"), Bost-Charles, Huber, Kontsevich,
  Brown, Fresán. p.58 Galois-cocycle form (p generic ⇔ φ(Gal) Zariski-dense in G) is correct, not in print in that
  shape, and anticipates the SHAPE of Deligne 1982 (absolute Hodge cycles = cocycle lands in Mumford-Tate group) - a
  historical detail. pp.11-13 checked (transcriptions): no self-correction about complex conjugation / real fields;
  p.11 = ordinary period conjecture containing Schneider's theorem, p.12 = elliptic questions. FROZEN.
- (old header) UNVERIFIED CANDIDATE · Grothendieck c.1969-71: "Conjecture de transcendance forte" for periods + Hodge decomposition
- Source: grothendieck.umontpellier.fr 18.pdf "Motifs et théorie de Hodge" (61 pp, [1969-c.1971]), p.10 (deep surprise 5).
  Possibly the missing "Hodge" section of the Motifs text (CSG U6d marks it "[[manque]]"; cf. L-012).
- Content (read by me, matches): tannakian motives over k ⊂ C with fibre functors T_B (over Q), T_DR (over k), T_Hdg =
  gr_F T_DR; motivic groups G'', G', G_k of dimension g; period torsors P = Isom(T_B⊗k, T_DR), Q ⊂ P' = Isom(T_DR, T_Hdg),
  P'' = Isom(T_Hdg, T_B⊗k); canonical complex points α (periods), β (Hodge decomposition), γ with βα = γ^{-1} etc.;
  U' ⊂ B' ⊂ G' (unipotent radical of the parabolic fixing the Hodge filtration), L' = B'/U', central Tate cocharacter j;
  Q = bundle of Levi subgroups of B'; Fil = Filt_⊗(T_B) ≅ G'/B' (dim g−b), Big = Bigr_⊗(T_B) ≅ G/L (dim g−l), Big → Fil a
  unipotent torsor (u + l = b). Boxed: "Conj. de transcendance forte — Si k ⊂ Q̄, alors deg.tr. k(α,β)/k = g + u" with
  consequences deg.tr. k(α)/k = g [the Grothendieck period conjecture], k(β)/k = u, k(γ)/k = g, K/k(β) = g, K/k(α) = K/k(γ)
  = u, Q(φ)/Q = g − b, Q(ψ)/Q = g − b + u = g − l (φ = period point in Fil, ψ = Hodge-decomposition point in Big);
  margin: "(2iπ)^n ∈ k(α) si Q(−n) ∈ Ob M".
- Why it might matter (interpretation): the period conjecture is known and credited to him (via André); the STRONG form
  adding β (periods + complex conjugates, i.e. the field of single-valued periods) with an exact transcendence degree
  g + dim U', and the exact-transcendence statements for the period point φ ∈ G/B and ψ ∈ G/L, are not known to me or
  to the reader from the literature (Schneider 1937 / Cohen, Shiga-Wolfart give only "algebraic iff CM" for φ).
- also cote 18 p.58 [5] (transcription only): the period torsor P = Isom^⊗(ξ_{M,k0}, ξ^Z_{M,v}⊗k0), the period cocycle
  φ_v(σ) = p^{-1}σ(p), and the reformulation "le point p de P_k est générique ⇔ Gal(k/k0) → G(k) a une image
  Zariski-dense" (margin "À vérifier / OK"). Sent to the running check as an extra fact.
- Caveats: conjecture sketch; André 2004 §23, Ayoub, Bertolin, Kontsevich-Zagier, Brown (single-valued periods),
  Deligne 1979 may contain it or a variant; Bakker-Tsimerman Ax-Schanuel is the functional analogue. NEXT: independent
  check (running).

### L-026 · CHECKED 4/10 (all 4 steps; FROZEN) · Grothendieck c.1968-71: "Conjectures 'Lefschetz' locales" for Chow groups of punctured spectra in all codimensions
- Independent check (2026-11-08): 4/10. Not formulated in print as such (SGA 2 XIII = local cohomology/π_1/Pic only; no
  "local Lefschetz" + Chow in codim ≥ 2 anywhere). Status by part: codim-1 injectivity "exc. p" for N ≥ 4 = Bhatt-de Jong
  2014 Thm 0.1 (bijectivity fails in general for non-CM); N = 2 = Mumford/Lipman; FALSE over C as written: "A^i(X)
  finite, J^i(X) = 0 for i ≥ (N+1)/2" and "N^i(X) finite for i ≥ N/2" fail for cone vertices (Mumford 1968 CH_0 of
  surfaces with p_g > 0; Griffiths 1969 / Clemens 1983 Griffiths groups; Schoen 1995 even over F̄_p); restriction ranges
  for i ≥ 2 = local form of Hartshorne 1974 / Paranjape weak-Lefschetz-for-Chow conjecture (open); numerical version of
  (1) for cones = Kurano 2004 Rem. 7.12 / Dao-Kurano 2014 Conj. 3.2 (conditional on standard conjectures); the critical-
  degree "intersection form" + Hodge-index reading for N = 3 = Hochster's θ pairing (1981), MPSW 2011 Ex. 3.12, Dao-
  Kurano Conj. 3.4 / Thm 1.2 (independently, uncredited); vanishing range i ≥ N/2 = Chow shadow of link semipurity
  (Steenbrink/Durfee/Gabber 1981-83) - a connection nobody wrote down. Archive: versos = Bourbaki exposé 391 (1970-71)
  -> written c.1971. Classification: missed connection + formulation-priority; usable only as a problem list. FROZEN.
- (old header) UNVERIFIED CANDIDATE · Grothendieck c.1965-71: "Conjectures 'Lefschetz' locales" for Chow groups of punctured spectra in all codimensions
- Source: grothendieck.umontpellier.fr 14.pdf "Théorie des cycles algébriques : conjectures de Hodge, Tate, Lefschetz, Weil"
  (131 pp, 1965-c.1971), p.105 (deep surprise 5), continued p.106.
- Content (read by me, matches): S = Spec A, A strictly local excellent, f ∈ m_A; X = S minus closed point, Y = X ∩ V(f),
  X, Y regular, U = X − Y, N = dim A. With A^i = Chow group, J^i = algebraically-trivial part, N^i = A^i/J^i:
  (1) N^i(X) ≡ 0 mod finite for i ≥ N/2; N^i(X) ≡ 0 and J^i(X) = 0 for i ≥ (N+1)/2 (so A^i(X) finite);
  (2) J^i(X) → J^i(Y) bijective "exc. p" for i ≤ (N−2)/2, injective for i ≤ (N−1)/2, zero for i ≥ N/2;
  N^i(X) → N^i(Y) bijective for i ≤ (N−3)/2, injective for i ≤ (N−2)/2, zero mod finite for i ≥ (N−1)/2;
  "Cas critiques J^{(N−1)/2}, J^{N/2}". (p.106 per reader: (3) A^i(X) vs A^i(U); (4) "Définir des formes 'intersections'
  N^i(X) × N^i(X) → Z ?? ... une théorie des cycles évanouissants"; N = 2 check = Mumford's finiteness of Cl mod alg. equiv.)
- Why it might matter (interpretation): higher-codimension version of the SGA 2 local Lefschetz theorems (Grothendieck-
  Samuel, codim 1 only); the vanishing ranges mirror the later weight/semi-purity results for links (Steenbrink, Durfee,
  Gabber); problem (4) prefigures Hochster's theta pairing / Kurano's numerical Chow groups of local rings. Higher-codim
  local Lefschetz for Chow groups is (per the reader) largely open.
- Caveats: conjectural only; SGA 2 Exp. XIII "Problèmes et conjectures" (1962) may already contain some of this (check);
  cote 14's cycles material is partly in Kleiman's 1968 "Algebraic cycles and the Weil conjectures" and the standard
  conjectures (1969). NEXT: (3) literature: SGA 2 XIII, Hartshorne "Ample subvarieties" ch. IV, Kurano, Srinivas, Kollár
  local Lefschetz for class groups, Ravindra-Srinivas; (4) independent check.

### L-025 · CHECKED 4/10 (all 4 steps; FROZEN under rule 9b) · Grothendieck 1975-76: integral divided-power de Rham model ("the lost manuscript", cote 136)
- Independent check (2026-11-07): 4/10. The core object is Cartan 1976 Example 4 (Invent. Math. 35, Dec 1976): Z<s><t_0..t_n,
  dt_i>/(Σt_i − s, Σdt_i) - the SAME homogenising variable (Cartan's s = Grothendieck's T), same year; also Miller 1978
  (Topology 17). Weight truncation ("shadows") = Cartan-Miller filtration property stated in Cenkl-Porter 1984. Steenrod
  operations from the PD complex (pp.13/181 programme) = Cenkl-Porter 1982, Cenkl 1989 (who also show "no commutative
  cochain problem solution over Z"). K(G_a,n) over F_p = Breen 1978. Grothendieck restated the whole programme publicly
  in Pursuing Stacks §94 (1983): "worked out independently by someone else too, I understand". The homotopy-type hope in
  fixed weight is FALSE (Steenrod obstruction; PD makes it worse: x^p = p!γ_p(x) = 0); he himself switched to binomial
  rings in PS §119 after Illusie/Breen - which is the KSZ 2023 theorem (that anticipation lives in PS, not here).
  Unpursued leftovers: the PD-triple (S,J,t) base change (p-adic case reinvented by Flynn-Connolly 2025, arXiv
  2501.10164, who cites Cartan), the "Omb(k)/Neg_∞" shadow categories, the topos-level PD-Koszul model - all weak
  prospects. => historical source for a lecture its author called lost; not lost mathematics. FROZEN.
- (old header) UNVERIFIED CANDIDATE · Grothendieck 1975-76: integral divided-power de Rham model of homotopy types ("the lost manuscript")
- Source: grothendieck.umontpellier.fr 136.pdf "Complexe de De Rham à puissance divisée [conférence de 1976 à l'IHÉS]"
  (375 pp, 1975-76; the Esquisse says he lent the manuscript of this lecture and it was lost, and that the intuition of
  "schematisation of homotopy types" germinated here). p.11 deep surprise 5; CSG: no scan, no transcription.
- Content (p.11, read by me, matches): C_DRpd(X_*,k) = bigraded divided-power de Rham complex over Γ_k(T) (simplex
  relation homogenised to Σt_i = T); "Remarques et Pbs a) ... C_DRS(X_*,k) ≃ C_DRpd(X_*,k)/(T-1) ... quel que soit k,
  C_DRS(X_*, k⊗Q) ≃ C_DRpd(X_*,k)/(T-1)"; PD-triple (S,J,t) base change; "b) Je suis convaincu que la structure p.d. sur
  l'idéal d'augmentation ... est importante" and the question whether, for simply connected X_* with finiteness
  conditions on H_i, C_DRpd(X_*,k) "avec toutes ses structures (y compris celles de p.d.)" determines the homotopy type.
- Modern context (interpretation): integral/algebraic models of homotopy types - Mandell 2006 (E∞ Z-cochains), Toën
  (schematization, "revisité" 2020), Horel binomial rings, Kubrak-Shuklin-Zakharov derived binomial rings.
- CONFIRMED (web, 2026-11-07): H. Cartan, "Théories cohomologiques", Invent. Math. 35 (1976) 261-271 = divided-power
  generalisation of Sullivan's forms over Z (same year as the talk; a 2025 arXiv paper on p-adic de Rham complexes,
  2501.10164, cites it as the standard reference). Cenkl-Porter 1984 (Pacific J. Math. 112) = tame cubical forms with
  filtrations, not divided powers. => the base construction is Cartan's; open for the check: the homogenised T / Rees
  form, the PD-triple base change, the "ombres" truncation theory, and the homotopy-type question.
- (earlier note) Novelty RISK (my memory, to check): H. Cartan, "Théories cohomologiques", Invent. Math. 35 (1976) builds integral
  de Rham forms on simplices with divided powers; Cenkl-Porter 1981-84 "tame" integral forms with divided powers and a
  weight filtration; Dwyer 1979 tame homotopy theory. If so the construction is known (possibly even influenced by/
  influencing Grothendieck's 1976 talk) and only the homogenised-T/Rees form and the "determines the homotopy type"
  question would remain. NEXT: finish 136 deep read; whole-cote summary; Cartan/Cenkl-Porter check; independent check.

### L-024 · CHECKED 5/10 (all 4 steps; FROZEN under rule 9b) · Grothendieck 1981: explicit "level-0" Grothendieck-Teichmüller relations
- Independent check (2026-11-07): 5/10. CONFIRMED: pp.2/7 are Drinfeld's relations (I),(II) up to normalisation (dictionary
  via Harbater-Schneps 2000 Thm A; exponent m=(λ-1)/2 hidden in the gauge of g), pentagon (III) absent. No pre-1990
  publication writes these non-abelian S_3-equivariance relations (Belyi 1979, Ihara 1986/89, Deligne 1989 checked via
  reviews/secondary sources). The literature says Grothendieck did not write them (A'Campo-Ji-Papadopoulos 2016 - NOT
  Lochak-Schneps, correction to my entry above; Lochak-Schneps 2006: "It is not known whether Grothendieck actually wrote
  down the defining equations"). BUT: Longue Marche Part II ("Variations sur l'équation des lacets", cote 140-3) has its
  table of contents (§41 "calcul des automorphismes extérieurs dans π̂_{0,3}", §44 "Mise en équations", §46 ...) and a
  typed §49 (129 pp) online at the Grothendieck Circle since 2003-05 (grothendieckcircle/LM/tableLM.pdf, 1lm_main.pdf);
  §49 contains "l'équation des lacets αρ(α)^{-1} = βσ(β)^{-1} l_1^ν ... ν = (μ-1)/2". So cote 145 = early draft of Part II
  §§41-49; the explicit equations have been publicly accessible for 20 years, just not read as such. => priority/
  historical fact only; no usable mathematics; (I)+(II) vs (III) question untouched. FROZEN. Possible unfinished area:
  ~600 untranscribed pp of Part II (metabelian envelopes, Fermat tower, "Approximations de Lie des systèmes de
  Galois-Teichmüller") - titles only; Schneps's survey calls §§38-53 a close study of the (0,3) and (1,1) cases.
- CORROBORATION (2026-11-07, cote 142 "Action de Galois sur Teichmüller", [1978-], p.24, deep [6] = first 6 of the run;
  read by me, matches): S_3-equivariant groupoid model of P^1-{0,1,∞} with six base points and half-loops; automorphisms
  parametrised by (ρ, β), ρ ∈ Ẑ^* "multiplicateur", γ = (ρ-1)/2 explicit; equations "(12) β σ_∞(β) = 1 ; α ρ^{-1}(α)
  ρ^{-2}(α) = 1 ; α = l_1^γ β" = Drinfeld's (I) and (II) exactly, with m = (λ-1)/2; "NB ... on retrouve les équations
  habituelles cf plus loin" (they were routine to him); τuτ^{-1} = (ρ, σ_∞(β)) with the request to verify directly that
  (12) is stable under β -> σ_∞(β); claim "β détermine ρ" (unproved; small open point). Same fact as L-024 in a
  cleaner form; rating unchanged (5/10; the typed Longue Marche §49 online since 2005 has the loop equation with
  ν = (μ-1)/2). No pentagon anywhere in cote 142 so far.
- also cote 142 p.38 [5]: same relations (70)/(70') β'σ_∞(β') = 1, α'ρ(α')ρ²(α') = 1 derived via an inclusion
  diagram (68) of seven base-point groupoids; same family, not viewed separately (rule 9b).
- LONGUE MARCHE PART 2 (cote 140-4, untranscribed; the area the L-024 reviewer flagged as possibly unexplored): p.220
  [5] = ms. p.758, §4 "approximation de Lie de (Π_0, 𝔊_0, M)": for a discrete "LT-group" 𝔊_0 (Teichmüller-type, with
  lacet homomorphisms K_i: T_0 ≅ Z → 𝔊_0 up to conjugacy) and a normal L-subgroup Π_0, a Zariski-dense φ: 𝔊_0 → 𝔊(Q)
  into an affine Q-group scheme with quasi-unipotent images of the T_0 defines a Q-algebraic GT-type group Γ^φ_Q → G_m;
  programme: compare these across a Teichmüller system (relative-completion flavour; Hain 1990s, Drinfeld's GT(Q),
  Deligne 1989). Setup only. Collect further part-2 pages, then one combined check at the end of batch 3.
  140-3 p.73 [5]: the hexagon relation with γ = (p−1)/2 derived from Ŝ = PSL_2(Z)^ (σ_∞² = (gρ)³ = 1), parametrisation
  (p, g_0 mod L_0) with relation I automatic via h_0 = [σ_∞, g_0^{-1}] - this is the "équation des lacets" section whose
  typed §49 is online (L-024 check); no new information. 140-3 p.77 [5]: the loop equation as a Z/3 nonabelian-
  cohomology problem in π̂_{0,3} with two orbit classes (ζ = λρ(λ)^{-1} and ζ = λ l_0^{-1} ρ(λ)^{-1}); case A pursued,
  case B left open (the cocycle formulation Lochak-Schneps 1997 rediscovered; see L-024 check). Same family.
  140-3 p.99 [5]: solutions parametrised by (g_0, γ), h_0 = g_0^{-1}σ_∞(g_0), hexagon ξρ(ξ)ρ²(ξ) = 1 with ξ = l_0^γ h_0;
  provisional facts π̂^{σ_∞} = 1 and coboundary characterisation. Same family. 140-3 p.101 [5]: conditions (63),(64),
  (68) + "conditions liminaires" for Aut(Ĉ⁺_{0,3}, σ_∞)' via (ξ, γ); Z/2 and Z/3 cocycle parametrisation with the λ mod 3
  split (Lochak-Schneps 1997 form); liminal conditions (pentagon-level?) left open. Same family. 140-3 p.129 [5]:
  2-cycle equation solved as unique coboundaries h = βσ_∞(β)^{-1} in the discrete case; needed profinite inputs
  isolated (no ρ-fixed elements in the completion; torsion of the completion conjugate to discrete torsion - later
  Scheiderer); geometric fixed-point picture via the triangular cartographic group. Same family.
  VERDICT on Longue Marche part 2 (140-3 + 140-4, 974 pp read): six [5]s, all the "équation des lacets" / GT-relation
  family already checked at 5/10 (typed §49 online since 2005) plus one "approximation de Lie" set-up page; nothing at
  6+; the §§50-52 material the reviewer flagged is set-up only. No further check (rule 9b). FROZEN with L-024.
- (old header) UNVERIFIED CANDIDATE · Grothendieck, spring 1981: explicit "level-0" Grothendieck-Teichmüller relations
- Source: grothendieck.umontpellier.fr 145.pdf "Printemps 81 (vieille rédaction)" (37 pp, 1981), pp.2 and 7 (deep
  surprise 5 each); pp.4-6 same topic (S_3 action on π̂_{0,3}, involution τ, products σ_iσ_j).
- Content (read by me, matches transcription): automorphisms u of π̂_{0,3} = profinite π_1(P^1 - {0,1,∞}) commuting with
  σ_0 and commuting exteriorly with the 3-cycle ρ are parametrised by p ∈ Ẑ^* and g_1 (mod ℓ_1): u(ℓ_1)=int(g_1)ℓ_1^p,
  u(ℓ_∞)=int(σ_0(g_1))ℓ_∞^p, with h_1 = σ_0(g_1)^{-1}g_1 and two relations: (1') ℓ_∞^p · int(h_1)(ℓ_1^p) ·
  int(ℓ_∞^γ ρ(h_1)^{-1})(ℓ_0^p) = 1 and (2) ρ(h_1) ℓ_∞^{-γ} h_1 ℓ_1^{-γ} ρ^{-1}(h_1) = ℓ_0^β, "où β, γ ∈ Ẑ sont uniquement
  déterminés par g_1, p"; gauge change g_1 -> g_1 ℓ_1^μ leaves β, γ invariant. p.7: (p, g) parametrisation from
  u(ℓ_0)=ℓ_0^p, uρ = int(g)ρu, giving the boxed relation ℓ_0^p · int(g)ℓ_1^p · int(gρ(g))ℓ_∞^p = 1.
- Modern reading (interpretation): the 2-cycle relation (built in via σ_0(h_1)=h_1^{-1}) and a 3-cycle/hexagon-type
  relation = Drinfeld's relations (I),(II) for GT̂ (1990), without the pentagon (III). Lochak-Schneps (arXiv 1603.03387)
  write that Grothendieck "realized that the image satisfies a certain number of simple equations, although he did not
  write them up" and that Drinfeld wrote them explicitly -> if these pages are not in the Longue Marche (cote 140,
  partly transcribed by CSG as G103d), the statement "did not write them up" is wrong and this is a priority fact.
- Longue Marche check (2026-11-07, CSG transcription G103d by URL, part 1 §1-37, ~300 printed pp, draft Feb 2026):
  explicit formulas NOT FOUND. Nearest: p.167 "Je n'ai pas vérifié que Γ → Aut_ext(π̂) soit injectif, cela m'empêche de
  faire des calculs dans Aut(π̂), fussent-ils heuristiques pour le moment"; p.169 "pour qu'il soit dans l'image de Γ il
  faut qu'il admette un relèvement u qui commute à ρ, et un relèvement qui commute à σ_0" (the condition, in words
  only). UNKNOWN: part 2 "variations sur l'équation des lacets" (cote 140-3, 695 pp, untranscribed) may contain it.
- Caveats: spring 1981 = the Longue Marche period (Jan-Jun 1981); the Longue Marche is known to contain a
  "computational formulation" of the Galois action on π̂_{0,3}; Ihara (1980s) and Drinfeld (1990) hold the credit for the
  explicit relations; mathematically fully superseded. NEXT: (3) check G103d transcription + Longue Marche literature
  (Schneps, Lochak, Ihara 1991 ICM) for these explicit relations; (4) independent check. No size until then.

### L-023 · DUPLICATE (published by Grothendieck himself: Esquisse d'un programme §5, footnote 7) · 1981-82 flag-indexed "déploiement" of stratified spaces
- VERDICT (2026-11-07): the Esquisse (1984, English transl. p.277, note (7)) states exactly this: "to reconstruct the system
  of spaces (i0,...,in) -> X_{i0,...,in} contravariant on Drap(I) (for the inclusion of flags), it suffices to know the
  X_i (or 'unfolded strata') and the X_ij (or 'joining tubes') ... X_ij -> X_j ('bounding' inclusions) and X_ij -> X_i
  (proper fibrations) ... the 'junction spaces' X_ijk ... hexagonal commutative diagram, where the two squares on the
  right are Cartesian ... composition map is given by the morphisms X_ijk -> X_ik". Cote 150 p.39 = draft of this
  passage. Barwick-Glasman-Haine, Exodromy (arXiv 1807.03281) acknowledgements already cite Grothendieck's stratified
  notes ([198]) and say "It is not clear to us how much of the work here he anticipated" -> the connection is KNOWN
  and flagged in print. Not missed -> DUPLICATE. LESSON: the deep reader marked the idea "not in Grothendieck's
  published texts" - wrong; check the Esquisse text first for any 1978-84 cote.
- (old header) UNVERIFIED CANDIDATE · Grothendieck 1981-82: flag-indexed "déploiement" of stratified spaces with a cartesian (Segal-type) condition
- Source: grothendieck.umontpellier.fr 150.pdf "Espaces stratifiés et voisinages côniques (ou : déploiement des espaces
  stratifiés)" (98 pp, 1981-1982), p.39 (deep surprise 5). Read by me: matches transcription.
- Content: a stratified space of type I (finite ordered set) is a contravariant functor Σ on flags d=(i0<...<in) of I into
  a category of spaces; restriction to an initial segment = fibration, deleting a non-last element = boundary embedding;
  condition (3): for flags d, d' with last(d)=first(d')=i and d''=d∪d', the square Σ_d'' → Σ_d', Σ_d → Σ_i is CARTESIAN;
  "Il suffit de le vérifier pour d et d' de longueur 2"; plus a transversality requirement; hence Σ_{i0...in} =
  Σ_{i0i1} ×_{Σ_i1} ... ×_{Σ_i(n-1)} Σ_{i(n-1)in}, so the whole structure is rebuilt from strata Σ_i, link bundles
  Σ_ij → Σ_i with boundary embeddings Σ_ij → Σ_j, and composition maps "Σ_ij ×_{Σ_j} Σ_jk → Σ_ik satisfaisant aux
  conditions" (left unfinished); margin: face/corner incidence rules in Σ_j.
- Deep reader's claim (interpretation, unverified): this is the Segal/"décollage" condition of Barwick-Glasman-Haine
  (Exodromy 2018; Haine arXiv 1811.01119) in a strict point-set form, bridging Thom-Mather control data and exit-path
  ∞-categories; the composition conditions and transversality are left open.
- Known context: the Esquisse (1984) §5 publicly announces the "déploiement" theory of stratified structures and says
  he developed "these dévissages" ~1982 (A'Campo-Ji-Papadopoulos quote) -> the IDEA is public; the question is whether
  the explicit flag/cartesian formalism is in the Esquisse or anywhere in print, and whether the 2018 authors knew it.
  Search so far: Exodromy/Haine results mention Grothendieck only via a conjecture used for reconstruction; no Esquisse
  citation found (not confirmed from the bibliographies themselves).
- NEXT: (2) read Esquisse §5 text on déploiement; (3) check Exodromy + Haine bibliographies; whole-cote summary of 150
  when its deep read finishes; (4) independent check. No size until then.

### L-022 · CHECKED 4/10 (all 4 steps; FROZEN under rule 9b) · Grothendieck's pre-Esquisse axiomatics of tame topology (cotes 120 + 121, 1974/1978)
- Independent check (2026-11-07, facts only): 4/10. FOR: dated concrete "structure"-type axiom systems (1974, 1978) for
  tame subsets of R^n, a correct Hardt-type trivialisation conjecture in 1978 (Hardt proved it 1980; Grothendieck
  still thought it unproven in 1984), a distinctive complement-free (regular-logic / FinSet-indexed) formulation, and
  "ind-objets spéciaux" anticipating Knebusch's weakly semialgebraic spaces (1989) - none described in print; the
  Esquisse only says "une dizaine d'années". AGAINST: every item is now a standard definition or theorem; the decisive
  o-minimality finiteness axiom is absent and triangulability is taken as an axiom (Esquisse admits this); the Esquisse
  already discloses the existence, approximate date, axiomatic character, field of tame constants and the dévissage
  theorem; the "families closed under projection/substitution" formalism was standard in logic (Tarski, Halmos's
  polyadic algebras 1950s) before 1974. No publication cites cotes 120/121 (not found). Caveat raised: a DCC on closed
  sets (121 pp.3-51) cannot hold for Euclidean semialgebraic sets -> the 1974 Boolean version was flawed or the
  transcription is lossy. Status: historical detail; not a tool for science now. FROZEN.
- (old header) UNVERIFIED CANDIDATE · Grothendieck's pre-Esquisse axiomatics of tame topology (Montpellier cotes 120 + 121, c.1974-78)
- Source: grothendieck.umontpellier.fr 121.pdf (72 pp, "Topologie modérée", inventory date "lettre (1974)"; p.35-36 refer
  to "la question relative à A'Campo" and A'Campo's thesis) and 120.pdf (24 pp, cover "Topologie modérée 1978? (Autour
  de l'Esquisse?)"). Deep-read flag: 121 p.54 surprise 5 (first >=5 page of the Montpellier run).
- What the pages say (read by me, p.54 image vs transcription: match): a "tame category" M with a conservative, finite-
  limit-exact functor X -> |X| to compact spaces + image axiom (p.53); extension to locally compact sigma-compact spaces
  by "ind-objets spéciaux" (monomorphic sequences with an interiority condition) giving "structure pseudo-modérée";
  proper pseudo-tame maps have pseudo-tame images; tame structure on R from one on I_1=[-1,1] stable under rational
  homotheties (R = "lim" I_n, transitions x n/(n+1)); axiom M4 (point 1, midpoint map, product map tame) => rational
  points tame, rational translations tame. Quote (p.54): "la catégorie des ind-objets [-spéciaux-] devient équivalente :
  celle des espaces loc. cpct pseudo-modérés". Cote 120 p.2-4: axioms M1-M4 for families M_n of subsets of R^n stable
  under projections/products/permutations/diagonals; p.22 field R_mod of tame points; p.24 "À prouver": generic
  piecewise-trivialisation of tame morphisms over a nowhere-dense tame Y' (= tame trivialisation / Hardt-type statement).
- Why it might matter (interpretation, unverified): this is a concrete axiomatic set-up for "topologie modérée" roughly
  10 years before the Esquisse (1984) and before o-minimality (van den Dries 1984, Pillay-Steinhorn 1986); the literature
  (A'Campo-Ji-Papadopoulos 2016 abstract; o-minimal histories) treats the Esquisse as Grothendieck's only statement.
  Scope hits: (b) finished-uncredited (an axiomatization), (c) connection (families M_n of subsets of cubes closed under
  projections = structural core of o-minimal "structures").
- Esquisse check (2026-11-07, EN text §5): Grothendieck says the problem "already began to intrigue me some fifteen years
  ago" (~1969) - "defining a theory of 'dévissage' for stratified structures" - and that he "returned to my reflection
  about stratified structures, from December 1981 to January 1982" (= cote 150); the Esquisse (§5-6) itself lists
  axioms (triangulability, tame parts of R^n, isotopic categories). => the EXISTENCE of 1970s reflections is public;
  what is not in print is the concrete 1974/1978 axiom systems (categorical M with functor to compacts; M_n families
  closed under projections/diagonals/products; M4-M8). Priority upside reduced accordingly.
- Caveats: the deep reader says the axioms as written are satisfied by all compact sets (not yet strong enough to force
  tameness); content is definitions/programme, few theorems; A'Campo (co-author of the 2016 history) was in contact
  with Grothendieck then and may know these notes; upside is mainly priority/history unless the compact-only, no-
  complement formulation is useful today. NEXT: (2) finish deep read of 120/121 and summarise the whole axiom system;
  (3) check A'Campo-Ji-Papadopoulos full text + van den Dries 1998 preface for any mention of pre-1984 notes;
  (4) independent unanchored check (subagent, facts only). No size until then.

### L-021 · NOTED, FROZEN (upside ~6: fragmentary) · Riemann 1861 prize-essay drafts: attempt at (contracted) Bianchi identity
- Cod. Ms. B. Riemann 9 (Wärmeleitung drafts, HS-3205052) fol. 4r: https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3205052:00000009/full/1600,/0/default.jpg
- READ BY ME: curvature components "(12,23)-(22,13)" etc.; cyclic schema "∂α(αβ,γδ) - ∂γ(αβ,δε) = ∂β(γδ,αε)";
  linearised divergence relations "∂γ(33) = ∂β(23) + ∂α(13)" (x3); attempted nonlinear corrections, third line blank;
  long unfinished p-symbol expression. = exploratory, incomplete attempt toward the differential/contracted Bianchi
  identity (Voss 1880, Ricci, Bianchi 1902; key for GR).
- Novelty: Cogliati 2014 (RHM 20, the main reassessment of the Commentatio) did NOT use the drafts and has no
  Bianchi-type content; Werke/Nachträge: not mentioned. Not independently checked (rule 9b: upside < 7, unfinished).

### L-020 · DUPLICATE (1/10) — Wirtinger published this exact sheet in 1902
- Riemann Werke Nachträge (1902, Noether & Wirtinger) §IV.G "Über Thetafunktionen, welche zu besondern Riemannschen
  Flächen gehören", pp.106-108 (signed W.): cites Akt 19 sheets 4'-6', dated "Göttingen, Oktober 1862"; describes the
  2p-2 zeros/sums, gerade/ungerade, formulas 1)-4) and 3*; "Hiernach steht es außer Zweifel, daß Riemann ähnliche
  Untersuchungen ... (Wirtinger 1895) geplant und teilweise durchgeführt hat". Ink of the date matches a Jan 1865 sheet
  -> date uncertain. Mumford, Prym Varieties I (1974) cites "Riemann, Nachtrag IV" -> "Riemann-Prym-Wirtinger-
  Schottky-Jung theory". Not new. (Scan: archive.org/details/bernhardriemann01riemgoog)
- LESSON: for Riemann Nachlass hits, check the 1902 Nachträge FIRST (Wirtinger reported on Akten 19, 25, 18, 26, 4
  -> L-019's Akt 26 (MN1853) and Akt 19 (AbelTheta) WERE examined by Wirtinger! -> re-check L-019 against Nachträge pp.110ff.)
### (old) L-020 · UNVERIFIED CANDIDATE (step 1 done; step 2 = literature match; 3-4 running) · Riemann Oct 1862: Prym/Schottky-Jung-type theta relations
- Cod. Ms. B. Riemann 19 (HS-3206670) fol. 87r, dated "Göttingen, October 1862":
  https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3206670:00000177/full/1600,/0/default.jpg
- READ BY ME: contour integrals of dlogΘ around cuts a_ν, a'_ν, b_ν, b'_ν on a two-sheeted cover; "e_ν = 1/2 Σ β_ν^μ +
  (h_ν+h'_ν)/2 πi + Σ (g_μ+g'_μ)/2 b_ν,μ"; parity "ϑ gerade/ungerade"; numbered claims "1) Ω(2u_1,…,2u_p,0…0) /
  ϑ(u)ϑ(u_1…u_p+πi/2) unabhängig von den Grössen u", "2) Ω(0…0,2v_1…2v_{p-1}) / (Θ(v))^2 unabhängig von den Grössen v",
  "3) …/Θ(v-e)Θ(v'+e) unabhängig von den Grössen e", "4) … wenn ϑ(c_1…c_p) = 0".
- Possible modern match: Schottky 1888, Wirtinger 1895, Schottky-Jung 1909, Fay 1973 ch.V, Mumford 1974.
- RISK: Wirtinger co-edited Riemann's Nachträge (1902) and worked on exactly this -> may be printed/known.
- NO SIZE until independent check returns.

### L-019 · PASSED ALL 4 CHECKS · 7/10 IF Riemann's hand & pre-1866 (8 if a handwriting expert confirms) · Riemann notes: energy-conserving shock relations + Prandtl-Meyer
- INDEPENDENT CHECK (2026-11-03): no published report of gas-dynamics/energy-conserving shocks in Riemann's
  Nachlass (Salas 2006/07 NASA preprint read in full; Haffner 2021; Papadopoulos 2017; Werke 1892 notes).
  Kalliope: Cod. Ms. B. Riemann 26, 252 leaves, "1853-1863, nur zum Teil datiert", contents listed =
  geomagnetism, Franklin-plate potentials, Riemann letter drafts; no other hand noted; gas dynamics NOT listed.
  KEY: Weber's 1901 edition DEFENDS Riemann's isentropic shocks ("im vollkommenen Einklang mit dem Gesetze der
  Energie"), no Hugoniot; only the 1912 5th ed. concedes "das Energieprinzip preisgegeben" -> Weber did not
  write these folios before 1901 and apparently never noticed them. No Prandtl/supersonic material in Weber.
  Riemann never published a correction; Rayleigh's objection 1877-78 (after his death). Notation φ'(ρ) = Riemann's
  (also Weber's) -> notation doesn't decide the hand. Weakeners: undated scratch work, unpublished, no influence;
  if before 1860 he may have considered and rejected energy conservation. To do: handwriting expert, dating,
  folios 72ff (74v gas equation-of-state thermodynamics).
- SECOND SHEET (2026-11-03): Cod. Ms. B. Riemann "Abel'sche Functionen [und Theta]" (HS-3206670, 1850-1865;
  fol. 1r dated April 1858) fol. 3v: https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3206670:00000008/full/1600,/0/default.jpg
  READ BY ME: axisymmetric compressible flow + Crocco-type dH relation; "2∫φ(ρ)dlogρ + ω^2 = aa = ω^2 + (λλ-1)φ(ρ)";
  "aa - bb sinφ^2 = aa - cc sinψ^2 = bc cosφ cosψ λλ"; "b sinφ = c sinψ"; "ψ - φ = α"; tgα/x formula; "s = 0",
  "s = ∞"; wedge sketch. VERIFIED (targets/riemann/verify/rat_3v_oblique_shock.py): oblique Prandtl relation
  follows from energy-conserving jumps; tanα formula + s-form correct; hypersonic limit tanα = (λ²-1)x/(1+λ²x²);
  max deflection sin α_max = 1/γ (45.58° for γ = 1.4) = textbook. => independent corroboration of L-019 from a
  different bundle; independent check on oblique-shock history running.
- INDEPENDENT CHECK #2 (oblique shocks, 2026-11-03): oblique-shock theory first = Meyer 1908 thesis (Prandtl);
  shock polar = Busemann 1929; Rankine/Hugoniot 1-D only. No report of shock material in Riemann's Nachlass found.
  HAND RISK raised: Kalliope lists other hands in HS-3206670 (= Cod. Ms. B. Riemann 19, 195 fol.): Weierstraß
  Bl.100-105, H. Weber Bl.115-120, Dedekind (envelope); none assigned to fol.3. Weber lived to 1913 (after Meyer
  1908); Bessel-Hagen/Siegel worked through the papers 1920s-30s in Prandtl's Göttingen -> later-hand copy of
  1906-08 work must be excluded. Rating stays 7/10 IF Riemann + pre-1866; ~0-1/10 value for science today.
- BLIND AI HANDWRITING COMPARISON (not expert; <local>/hand_compare.out): 5 unlabelled pages: 70r (P1),
  Weber 115r (P2), Riemann Primzahlen 36r (P3, accepted Riemann zeta notes), AbelTheta 3v (P4), Riemann letter
  draft 92r (P5, pencil). Result: P1-P4 same hand (high), P1-P3 same (medium), P3-P4 same (medium-high);
  Weber P2 probably DIFFERENT (medium; fair-copy caveat); P5 undetermined (pencil prose). => supports Riemann's
  hand; still needs a human palaeographer (SUB Göttingen manuscripts dept.).
- MY OWN SIDE-BY-SIDE HAND COMPARISON (2026-11-03; non-expert; IIIF crops in <local>/gimg/crop_*.jpg):
  reference = Riemann's DATED air-wave draft Luftwellen 65r ("Juni 1856" / "October 1857", same topic, same
  notation). Shared specific forms with 70r and 3v: ρ written as a looped ς-shape with left-curling descender
  (65r "ρ1(x'1 - ∂x/∂t)", 70r "v1ρ1", 3v "dlogρ"); connected doubled "aa" (65r "aa(ρ1-ρ2)", 3v "aa - bb");
  same looped ∂; same slant, ink and fast cursive. Weber 115r (fair copy): more upright, evenly spaced, long
  radical overlines; no ρ/aa to compare. => my comparison SUPPORTS Riemann's hand; not proof.
- 1902 NACHTRÄGE CHECK (read by me, archive.org bernhardriemann01riemgoog, "Bericht über die Akten Nr. 19, 25 (mit
  18), 26, 4", pp.110-113, signed N./W.): Noether & Wirtinger describe Akt 19 (Hefte 19α-δ: P-functions, function
  theory, Abelian/theta incl. "Italien. ϑ-Funktionen") and Akt 26 "Varia" (47 loose sheets: early physics notes,
  naturphilosophical calculations, number theory, 1858 elasticity/electricity lecture, habilitation drafts, Franklin
  plate, ϑ-functions, Nobili rings, elliptic cylinder, reciprocity law, "Vorschlag zu einer ... hydrodynamischen
  Preisfrage", Gradmessung, thesis drafts). NO mention of gas dynamics, shocks, Luftwellen or supersonic flow.
  => the 1902 editors surveyed both folders containing the L-019 sheets and did not report them (overlooked or
  not recognised). Strengthens novelty.
- BLIND HANDWRITING TEST WITH CONTROLS (2026-11-03; <local>/blind_key.json, blind_hands.out): 11 shuffled,
  unlabelled pages: 4 known Riemann (Luftwellen 65r dated 1856/57, Luftwellen 69v, Primzahlen 36r, MN1853 52v
  pencil), 2 catalogued Weber (Riemann 19 Bl.116r, 118r), 2 catalogued Weierstraß (Bl.101r, 103r; Schlesinger
  1920 note), 3 shock pages (70r, 71r, 3v). RESULT: 3 writers recovered CORRECTLY - Weber pair together (high),
  Weierstraß pair together (high; same-topic Abelian material, so separation was by hand, not topic), Riemann
  refs together; ALL 3 SHOCK PAGES clustered with the Riemann references (high), incl. with the zeta page
  (different topic, medium-high). Only miss: Riemann pencil page 52v "tentative" (medium/pencil). Caveat: model
  may partly use shared notation (∫φ(ρ)dlogρ, aa doubling) - but notation habits are themselves authorial.
  => strong (non-human) evidence the shock sheets are in Riemann's hand, not Weber's or Weierstraß's.
- NEW CONTEXT (read by me, Luftwellen 65r, October 1857): "Verlust an lebendiger Kraft aa (ρ1+ρ2)/2 (x'1 - x'2)^2 dt"
  and "geleistete Arbeit aa(ρ1x'1 - ρ2x'2)dt" -> in 1857 Riemann explicitly computed the LOSS of kinetic energy at
  an (isothermal) discontinuity. So he knew his jump lost mechanical energy before publishing (1860); the L-019
  sheets are the energy-conserving alternative. (Weber 1892 notes say formulas were "angedeutet in Riemann's
  Papieren" -> the 1857 loss computation may be known to editors; the L-019 sheets were not reported.)
- CONTEXT from Riemann's "Konzepte und Notizen zu Luftwellen" (HS-3205096, transcribed 2026-11-03; machine
  transcription, not yet read by me): drafts of the 1860 paper; 65r dated June 1856 (Riemann-function method) and
  October 1857 (discontinuities: "geleistete Arbeit aa(ρ1x'1 - ρ2x'2)dt", case analysis of how a discontinuity
  splits); 69v Boyle-law (isothermal) shock conditions; 32r/34r: k = c/c' from the mechanical equivalent of
  heat (A = 423.55), Regnault and Joule, Mayer hypothesis. => in 1856-57 drafts he uses isothermal/isentropic
  jumps but is thinking about work and heat. L-019's sheet (polytropic k + energy flux) is NOT among these
  drafts; its relation in time to them is unknown (hypothesis only: later, possibly after 1860).
- READ BY ME (71r): "e^{4ri} = e^{2σi}(y+i)/(y-i)((y-λi)/(y+λi))^λ, y = √(ω^2/φ'(ρ) - 1), ω^2 = aa(1+yy)/(λλ+yy),
  φ'(ρ) = aa/(λλ+yy)"; boxed simple wave ("r = const"); "2k/(k-1) p1/ρ1 + v1^2 = v1v2λλ = 2k/(k-1) p2/ρ2 + v2^2";
  small sketch at bottom: a channel (rectangle) with rays fanning from its corner (expansion fan picture).
- VERIFIED (targets/riemann/verify/r53_71r_prandtl_meyer.py): Bernoulli parametrisation correct; dν = √(M²-1)
  dlog ω; ν(y) == textbook Prandtl-Meyer ν(M) exactly.
- DATING EVIDENCE (2026-11-08, read by me): the oblique-shock sheet Riemann 19 fol. 3v is the VERSO of a leaf whose
  recto 3r (canvas 7) carries the same April-1858 theta project as fol. 1r (dated "April 1858"), 2r, 2v, 4r, 4v
  (elimination of X = √(xy)+√(zt)+√(uv) = 0 with parameter s, binary characteristics). 3r ALSO has a vertical Italian
  marginal note in a different, upright hand: "Ma se ha finito, deve pagare per tutto il tempo. Ciò andrebbe
  regolarizzato" (my reading) -> the leaf was still in use in Riemann's Italian years (late 1862 - 1865/66). So 3v ∈
  [1858, July 1866]; the Italian note + the Pisa 1863-64 items near fol. 70-71 in Riemann 26 favour reading (ii): the
  energy-conserving/oblique shock work as an unpublished post-1860 correction, written in Italy. Independent check #3
  (dating + fol. 70v Crocco-type vorticity relation + 71v 2-D characteristics) RUNNING.
- READ BY ME (2026-11-08) fol. 70v (canvas 142): "2p₂/ρ₂ + v₂²(1−1/k) = v₁v₂(1+1/k) = 2p₁/ρ₁ + v₁²(1−1/k)"; "2p/ρ + ω²(1−1/k)
  = const"; "dp/ρ + ω dω = dσ (1/ρ)(∂v/∂x − ∂u/∂y)"; "d_ρ log p = k d log ρ"; "(1−1/k)(dp/ρ + ω dω) = −(1/k) d_σ p/ρ";
  "(1/ρ)(∂v/∂x − ∂u/∂y) = −1/(k−1) ∂p/∂σ" [vorticity = entropy gradient across streamlines, Crocco 1937 form]; then
  p = ρ^k/φ'(σ) with f(σ) = φ'(σ)^{k−1}, and the full nonlinear stream-function equation (c r² − (k+1) r^{k+1})Δψ −
  ψ_x²ψ_xx − 2ψ_xy ψ_x ψ_y − ψ_y² ψ_yy = r^{k+1}(1−1/k) ∂log φ'(σ)/∂σ (c r² − (k+1) r^{k+1}) [rotational compressible
  stream-function equation with entropy source, 1940s form]. fol. 71v (canvas 144): √(ω²/φ'(ρ) − 1) [= √(M²−1)] as the
  Mach-angle factor; characteristic directions (u ∓ v√…, v ± u√…); integrating factor Ω; "ω²/φ'(ρ) − 1 = −∂log(ρω)/∂log ω";
  second-order equation √(M²−1) ∂²w/∂r∂s + ½ ∂log(ρ√(M²−1))/∂log ω (∂w/∂r + ∂w/∂s) = 0 in characteristic coordinates
  (r, s); polar form u = ω cos δ, v = ω sin δ [method of characteristics for steady 2-D supersonic flow, Prandtl-
  Busemann 1929]. Transcriptions match.
- VERIFIED BY CODE (2026-11-08, targets/riemann/verify/r26_70v_71v_crocco_characteristics.py): 70v chain R1-R3 and
  dp/ρ + ω dω = −(1/(k−1)) d_σp/ρ all hold for p = ρ^k g(σ) with uniform total enthalpy; Euler identity gives
  dp/ρ + ω dω = ∓(ζ/ρ)dσ, hence ζ/ρ = ±(1/(k−1)) ∂p/∂σ /ρ (sign = convention of σ) = Riemann's line; 71v: level lines
  of r make angle μ with the velocity with sin μ = 1/M exactly (Mach lines); mass-flux relation ω²/c² − 1 =
  −∂log(ρω)/∂log ω holds. So pages 70r, 70v, 71r, 71v, 3v are now all read by me and code-checked.
- INDEPENDENT CHECK #3 (2026-11-08, dating + 70v/71v): rating 7/10 NOW (the "before 1866" condition is substantially
  met; content broadened to five named results), CEILING 9 if a human expert confirms (a) 3v is the same hand/ink
  campaign as 3r (certainly Riemann) and (b) three lines read as transcribed: the "(1 + 1/k)" Prandtl line on 70v, the
  d_σ(p/ρ) cross-streamline term on 70v, the v₁v₂ parametrisation on 3v. Expected value ~6.5 (reviewer's weights:
  c.1856-60 55%, 1860-66 30%, not Riemann's hand 15%). Dating: 3v ∈ [c.1856, July 1866]; the recto date does not fix
  the verso (the Italian note proves two writing campaigns on the leaf); bundle 19 was in use "Piano bei Pisa" per the
  DDB record. The 1860 paper (TeX source checked) has no "Energie/lebendige Kraft" and quarantines thermodynamics
  ("Wärmeaustausch ganz zu vernachlässigen"; 1859 notice: a PDE contribution) -> the 1857 energy-loss computation was
  deliberately left out, and the sheets' notation (φ(ρ), aa, k, ∫…dlogρ) is Riemann's 1856-60 system, not Prandtl's
  (c*, κ, M) - a real point against a post-1904 hand. 70v = Crocco's theorem (1937; Friedmann 1922 first statement)
  specialised to steady 2-D polytropic flow behind a curved shock, no 19th-c. precedent found; 71v = Mach-line
  characteristics with integrating factor (Prandtl 1904/07, Meyer 1908, Prandtl-Busemann 1929), a routine extension
  of his 1860 method. What would LOWER it: different hand/ink on 3v vs 3r; human transcription showing the energy
  lines are the 1860 §5 forms; any anachronistic symbol (M, c*, κ, γ) or post-1866 citation; 1890s-1900s paper;
  fol. 74v being a van der Waals form with a b-term; the pages being a reader's copy (precedent: Clebsch's copy of the
  1859 paper in Riemann 3). Discriminating checks for SUB staff: ink/pen continuity 3r-3v; whether 3-4 is a bifolium
  and 4r continues 3r; watermark of fol. 70-71 vs the 1857 Luftwellen sheets; a full pass through bundle 21 for
  energy-conserving forms on DATED sheets.
- 74v CHECK (2026-11-08, transcription): empirical equation of state log ϑ = log p + log v + a/v + bp + c/v² + dp² + ep/v,
  c_p − c_v = A(...), and "log ϑ = log(p + α/v²) + log 𝔙(v)" - a Laplace/Hirn-type internal-pressure form with NO (v − b)
  covolume term -> no van der Waals (1873) anachronism; 74r = rotation ODEs + Christoffel-type symbols (1861
  Commentatio material) -> the neighbourhood of fol. 70-71 is consistent with c.1861. Email draft updated.
- Experts (maintainers decide): Olivier Darrigol (historian of hydrodynamics, "Worlds of Flow"); Manuel D. Salas
  (shock-wave history); Riemann Nachlass specialists (Arias de Reyna, Gabcke, Neuenschwander) for the hand.
### (old) L-019 · UNVERIFIED CANDIDATE (steps 1-2 done; 3-4 running) · Riemann notes: energy-conserving shock relations + Prandtl-Meyer
- Cod. Ms. B. Riemann "[Mathematische Notizen] 1853-1863" (HS-3206190) fol. 70r/70v/71r/71v:
  70r https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3206190:00000141/full/1600,/0/default.jpg
  71r https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3206190:00000143/full/1600,/0/default.jpg
- READ BY ME (70r): "∫φ(ρ)dlogρ + u^2/2 = k/(k-1) p/ρ + u^2/2"; energy-balance bracket with (k-1); "p1 - p2 =
  v1ρ1(v2 - v1)", "p1 + p2 = (1/k) v1ρ1(v1+v2)", "2p1/(v1ρ1) = v2(1/k+1) - v1(1-1/k)", "2p2/ρ2 + v2^2(1-1/k) =
  v1v2(1+1/k) = 2p1/ρ1 + v1^2(1-1/k)"; then dp/ρ + ω dω = (v dx - u dy)(∂v/∂x - ∂u/∂y) = -1/(k-1) dσ p/ρ.
- VERIFIED (targets/riemann/verify/r53_70r_shock.py): all relations follow from mass+momentum+ENERGY
  (Rankine-Hugoniot); the key relation FAILS for an isentropic jump (Riemann 1860's condition).
- Deep reader (not yet by me): 71r Prandtl-Meyer function + centred expansion fan; 71v hodograph (Chaplygin).
- RISKS: hand (Riemann vs editor Weber, whose 1900/01 book uses Hugoniot); date; prior reports.
- NO SIZE until independent check returns (rule 9c).

### L-018 · CHECKED 5/10 (all 4 steps; FROZEN under rule 9b) — independent check 2026-11-03:
- (B) constant 0.02309 57089 66121 03381 + formula already PRINTED by Siegel 1932 (§4; Eng. tr. arXiv 1810.05198).
  ψ-form of explicit formula (von Mangoldt 1895) = short rewrite of 1859 formula -> (B) alone ~3/10.
- (A) L-function functional equation: earlier/near cases exist - Malmstén 1849, Schlömilch 1849, Eisenstein 1849
  (mod 4); KINKELIN 1862 (prime-power / odd squarefree moduli, i.e. covers prime q, within Riemann's lifetime);
  Hurwitz 1881/82 (real characters); Lipschitz 1889 (general primitive characters with Gauss sums). Possible
  novelty = general COMPLEX characters with Gauss-sum factor, |τ|^2 = q and completed ξ_q, before 1889.
  Not found in Siegel, Werke/Nachträge, Arias de Reyna 2024/2026, Hurwitz survey (arXiv 1506.00856). RISK:
  Arias de Reyna/Gabcke hold scans of all Riemann number-theory papers -> may know it unpublished.
  Unchecked: Edwards 1974, Neuenschwander 1988, Narasimhan 1990 edition.
### (old) L-018 · UNVERIFIED CANDIDATE (steps 1-2 done; steps 3-4 running) · Riemann: L-function functional equation + von Mangoldt's psi formula
- Cod. Ms. B. Riemann 3 "Primzahlen" fol. 36r: https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3226542:00000071/full/1600,/0/default.jpg
- READ BY ME: "χ(s) = Π 1/(1 - p^-s α^{Ind p}) = Σ α^{Ind n}/n^s (mod q)", contour derivation with Gauss sums,
  "Σ ρ^n α^{Ind n}/√q · Σ ρ^-n α^-Ind n/√q = 1", completed "Π(s/2-1) q^{s/2} √(Σ q^-1/2 ρ^n α^-Ind n) π^-s/2
  Σ α^{Ind n}/n^s = ξ_q(t)"; "ψ(x) = x - Σ(x^{1/2+αi}/(1/2+αi) + x^{1/2-αi}/(1/2-αi)) - 1/2 log(1-1/x^2) - log 2π";
  "Σ 1/(αα+1/4) = 0,02309 57089 66121 03381"; ∫ψ dx; Laplace start.
- VERIFIED (targets/riemann/verify/r3_36r_checks.py): constant = 0.02309570896612103381431 (Riemann's 20 digits
  correct up to last-digit rounding); log π, log 4, (log 4π - C)/2 to 20 digits correct; ψ formula = textbook
  von Mangoldt formula; Gauss-sum identities hold.
- Usual credit: Hurwitz 1882 (L-function functional equation, general χ), von Mangoldt 1895 (ψ explicit formula).
- NO SIZE until independent check returns (rule 9c).

### L-017 · CANDIDATE (medium, upside ~6-7; READ BY ME; novelty doubtful) · Gauss: Givens-rotation least squares c.1807-10
- HB "Kleine Aufsätze" p.[50] (canvas 60): https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3352584:00000060/full/1600,/0/default.jpg
- READ BY ME: "Methode der kleinsten Quadrate": Ω = (λA)^2 + (μB)^2 + (μ'B')^2 + ... minimum; "Man setze α/β = l,
  μ/(λl) = tang φ ... A + kB = A', A - lB = C, λcosφ = λ', λsinφ = ν, so ist (λ'A')^2 + (νC)^2 = (λA)^2 + (μB)^2 und
  C von x frei ... Fährt man auf dieselbe Art weiter fort, so erhält Ω die Gestalt Ω = (νC)^2 + (ν'C')^2 + ... wo alle C
  von x frei sind" = sequential 2x2 orthogonal (Givens) eliminations on weighted observation equations.
- Usual credit: Jacobi 1846 (plane rotations), Givens 1954/58, Golub 1965 (orthogonal LS).
- NOVELTY RISK: pencil "Kr" marks on the page (likely Werke editor L. Krüger, Werke IX geodesy 1903) -> may be
  printed/discussed. Web search: nothing. Check Werke IX/XII + Stewart's afterword before any more work.

### L-016 · VERIFIED REAL BUT MODEST (4/4 checks done; independent rating 5/10; FROZEN under rule 9b)
- INDEPENDENT CHECK (subagent, facts only, 2026-11-03): re-derived coefficients exactly; NO prior art before
  1810-16 for a self-gravitating Boyle-law gas (Newton Principia II prop.22 = external centre; Legendre-Laplace
  = n=1 density law, Laplace 1825); Kelvin 1887 said the isothermal problem was "first, I believe, proposed by
  Tait" (1885 exam). Usual credits: Zöllner 1871 (1/r^2 solution), Ritter 1882, Darwin 1889, Emden 1907;
  Lane 1870 = polytropes, not isothermal. Not found in Werke V (full text), X.1/XI.1/XII (TOC only), modern
  histories. WEAKENERS: notebook used 1809-1835 (DDB record) -> page date needs page-level evidence; series
  routine once equations written; no physical interpretation, no influence. Rating 5/10 (real ~60-yr priority
  over Zöllner/Ritter; short history-of-astronomy note). Up if firmly dated + letters show it was his own;
  down to ~3 if after 1830.
### (old header) L-016 · STRONG CANDIDATE (READ BY ME + VERIFIED EXACT; novelty: not in Werke II/III/V, not online) · Gauss solves the self-gravitating isothermal gas sphere (Lane-Emden / Emden equation) c.1810-1816
- Source: Gauss Handbuch "Kleine Aufsätze aus verschiedenen Theilen der Mathematik. Angefangen im May 1809"
  (Cod. Ms. Gauß, GDZ DE-611-HS-3352584), p. 89 (canvas 99):
  https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3352584:00000099/full/1600,/0/default.jpg
- READ BY ME: heading "Vertheilung einer elastischen Flüssigkeit die sich blos durch ihre eigne Attraction
  zusammenhält". First attempt -dp = m p dr, dm = p rr dr (gravity ~ m), q = 1/p, ddq/dr^2 = (1/q)(dq/dr)^2 + rr,
  series for q and t = sqrt(q). Then "Oder richtiger: -dp = m p dr / rr, dm = p rr dr" (Newtonian gravity,
  pressure ∝ density = Boyle) with p = 1 - rr/6 + r^4/45 - 61 r^6/22680 + 629 r^8/2041200 [- 2869/(346500.243) r^10],
  1/p, m, r^3/(3m) series; "Einfacher geschrieben" p = 1 - 1/2.rr/3 + 1/5.r^4/9 - 61/840.r^6/27 + 629/25200.r^8/81
  - 2869/346500.r^10/243.
- VERIFIED: targets/gauss/verify/hb09_89_isothermal_sphere.py - exact rational solution of -p' = m p / r^2,
  m' = p r^2, p(0)=1: coefficients r^0..r^10 ALL equal Gauss's (1, -1/6, 1/45, -61/22680, 629/2041200,
  -2869/84199500). (Deep reader notes small slips in his 1/p and r^3/3m side series.)
- Modern meaning: this is the isothermal Lane-Emden (Emden-Chandrasekhar) equation (1/r^2)(r^2 psi')' = e^-psi,
  p = e^-psi, with its central series - the founding model of stellar structure / isothermal spheres
  (stars, globular clusters, dark-matter halos, Bonnor-Ebert spheres).
- Usual credit: J. Homer Lane 1870 (polytropic gas sphere, Sun), A. Ritter 1878-83, Lord Kelvin 1887,
  R. Emden "Gaskugeln" 1907 (isothermal sphere); Chandrasekhar 1939.
- DATING: page labels 71-79 dated 1810 (one 1812); 97-98 dated 1816-1818 -> p.89 c.1810-1816. => ~55 yrs
  before Lane, ~90 before Emden.
- Novelty: Werke II, III, V (physics) text search: no hits for the heading/phrases; web search: nothing on Gauss
  + isothermal/Lane-Emden. UNCHECKED: Werke X.1, XI.1 (1927, physics/astronomy Nachlass), XII (1929 varia);
  histories of the Lane-Emden equation (Chandrasekhar 1939 historical notes; Horedt 2004 "Polytropes").
- Size if confirmed: Gauss had the basic equation of stellar structure decades before it was "invented".
  ~7/10 history of science/astrophysics; public ~4-5/10 (Gauss + stars = story). Experts (maintainers decide):
  historians of astrophysics; Gauss-Gesellschaft Göttingen.

### L-015 · CANDIDATE (READ BY ME + VERIFIED to O(z^80); dating caveat) · Gauss: Jacobi's 3rd-order ODE for theta3 (Jacobi 1847/48)
- Math.25 fol. 84v (+84r): https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3381838:00000171/full/1600,/0/default.jpg
- READ BY ME: "Setzt man anstatt z, e^ξ, dξ constant so werden die Gleichungen 0 = (UU-TT)/(TU^4) + 4T'',
  0 = (UU-TT)/(UT^4) - 4U''"; "Diese wird integrabel wenn man mit UT'-TU' multipl."; "2(UT'-TU')^2 =
  1/2(TT/UU + UU/TT) + Const. Die Constante findet sich = -1"; T = p^-2 ...; "4p'/p - 4q'/q = r^4";
  "p^6q^4 - ppq^8 - 8pp'' + 24p'p' = 0"; final "(pp''-3p'p'){10p'/p - p^4 + 2q^4} + 5p'p'' - pp''' = 0";
  pencil: q^4 = 1/2 p^4 ± 1/2 sqrt(p^8 - 32p''/p + 96p'p'/pp) -> eliminating q gives an ODE in theta3 alone.
- VERIFIED: targets/gauss/verify/m25_84v_theta_ode.py (exact rational series, O(z^80)): all three ink equations hold.
- Modern: Jacobi, Crelle 36 (1848) "Über die Differentialgleichung, welcher die Reihen 1 ± 2q + 2q^4 ± ...
  Genüge leisten" (3rd-order nonlinear ODE for theta constants); Halphen 1881; Chazy; Brezhnev et al.
  (arXiv 1012.1429) on "a little-known dynamical system obtained by Jacobi".
- Novelty: Werke III theta Nachlass (OCR via API): no recognizable 3rd-order ODE; no nome-derivatives of the
  AGM relation. Web: nothing on Gauss. UNCHECKED: Werke VIII, X.1, Schlesinger (X.2).
- CAVEAT: undated; Gauss lived to 1855 and could be re-deriving Jacobi's 1848 paper. Neighbouring pages (84r)
  derive it from the hypergeometric equation for theta3^2 (= 2K/pi) - a different route from Jacobi? (check).
- Size if earlier than Jacobi: medium (~5/10), pairs naturally with L-014 as "Gauss's theta notebook".

### L-014 · DEAD / KNOWN (independent check 2026-11-03: rating 1-2/10)
- Jacobi, Fundamenta Nova (1829) p.186 cube identity + p.187 expansion of the reciprocal theta product into
  simple fractions ("e nota theoria resolutionis ... facile obtinentur") -> geometric expansion gives Gauss's
  coefficients. Biehler 1879 thesis (Part III §§47-53): Jacobi "le premier" to expand 1/Θ; Cauchy C.R. XVII
  (1843) derived the coefficients; Appell 1884 general class. Modern: Andrews-Garvan 1988 (Lerch-sum form).
  MY "MOCK THETA" FRAMING WAS INACCURATE: coefficients of 1/θ are false/partial theta / η^3 -> quantum/false
  modular forms, not mock theta. Only residual interest: if page predates 1829 (undated; Schlesinger dates the
  P(x,y) "Hundert Theoreme" notation after 1818) -> one more "Gauss before Jacobi" instance. Not pursued.
### (old header) L-014 · CANDIDATE (READ BY ME + VERIFIED to O(x^60); novelty: not in Werke III, not found online) · Gauss: Fourier coefficients of 1/theta (Appell-Lerch / mock-theta type)
- Math.25 fol. 67r: https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3381838:00000136/full/1600,/0/default.jpg
- READ BY ME: "[1 + x(y+1/y) + x^4(yy+1/yy) + x^9(y^3+1/y^3) + etc.][a + b(y+1/y) + c(yy+1/yy) + ...] = 1";
  the infinite linear system; series a = 1+2xx+6x^4+14x^6+32x^8+66x^10, -b = x+3x^3+8x^5+19x^7+42x^9+87x^11,
  c, -d, e, -f; then closed forms a = (1-xx+x^6-x^12+x^20)/(1-3xx+5x^6-7x^12+9x^20),
  b = (x-x^5+x^11-x^19+x^29)/(same), c = (x^2-x^8+x^16-x^26+x^38)/(same), d = (x^3-x^11+x^21-x^33+x^47)/(same)
  [sign of b, d: Gauss's -b, -d convention]. Also Q(x,y)/P(x,y) = 1/(Px.Qx){1 - 2(y+1/y)/(x+1/x) + 2(yy+1/yy)/(xx+1/xx) - ...}.
- Modern meaning: Fourier coefficients of 1/theta_3(z) = (-1)^k sum_{n>=0} (-1)^n x^(n(n+1)+|k|(2n+1)) / (x^2;x^2)^3
  = partial theta / eta^3-type: the prototype "meromorphic Jacobi form" whose coefficients are mock modular
  (Zwegers 2002); Appell-Lerch sums (Appell 1884, Lerch 1892). A 2022 survey (arXiv 2202.03329): the universal
  mock theta function g3 of Gordon-McIntosh "arises naturally from the reciprocal of the classical Jacobi
  triple product".
- VERIFIED: targets/gauss/verify/m25_67r_inverse_theta.py - identity holds to O(x^60) for y^-6..y^6; all six of
  Gauss's tabulated series correct.
- Novelty: Werke III theta Nachlass (OCR, read by API): NO expansion of 1/P, NO partial-theta-over-cube form, NO
  Appell-Lerch sum. Extended web search: nothing on Gauss + 1/theta. UNCHECKED: Werke VIII (1900, Fricke),
  Werke X.1 (1917) Analysis pp.137-450, Schlesinger's essay (X.2 Abh.2); Lemmermeyer. Undated (Math.25 =
  lemniscatic/theta bundle; Gauss's theta work mostly 1798-1820s).
- Size if new: earliest known Appell-Lerch-type / "mock" object, decades before Appell (1884). ~5-6/10 in
  q-series / mock-modular community; good story (Gauss -> Ramanujan's mock thetas). Not new mathematics.

### L-013 · PARKED (medium; novelty search clean; not hand-verified) · Gauss: Kummer-style units of Z[zeta_5]
- Math.16 fol. 5v [5] https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3376639:00000010/full/1300,/0/default.jpg
  (+ 8r [4] :00000017, 12r [4] :00000025). Deep reader: proof that a cyclotomic unit u satisfies u/ū = ε^n
  (Kummer's lemma special form), the question whether cyclotomic units generate all units, λ-adic analysis of
  units of Z[ζ5] (unit ≡ 1 mod λ^3 => ≡ 1 mod 5), norm form + golden-ratio unit reduction. Usual credit: Kummer
  1840s-1850. Known: Gauss's n=3 Eisenstein-integer FLT fragment (Werke II), 1816 letter to Olbers.
- Novelty: 1 web search, nothing crediting Gauss. Check Lemmermeyer (Reciprocity Laws; arXiv) before any work.
- Size: medium (Gauss's interest in FLT via complex integers is known). Undated.
- Also: Math.16 1v/2r [4] = Hermitian forms over Z[i] for four squares (adds to L-010); 2r's neighbour cites
  Jacobi in Crelle 3 and 12 -> L-010 material dates >= ~1834, before Hermite 1854.

### L-012 · STRONG CANDIDATE (READ BY ME; novelty: not in literature checked) · Grothendieck's lost "Hodge" part of Motifs: p-adic variational Hodge conjecture + a framework for it
- Source: CSG scan "Motifs" (ca. 1966 per CSG; no cote given), 10 pp pencil on squared paper, stamp "21445"(?)
  top right: https://csg.igrothendieck.org/wp-content/uploads/2025/11/U121.pdf (uploaded Nov 2025; untranscribed).
  Local images: <local>/u121/p01-p10.jpg (extracted as data; PDF has no JS/Launch).
- READ BY ME (pp.7-10):
  p.7 "Suite du Frobenius" ... "D'où notion de F-cristal"; "Mystère de Tate-Hodge-DeRham: Trouver deux
    sous-catégories pleines P ⊂ a) des DR-F-cristaux (sereins) sur X^ (il n'y a plus de X), Q ⊂ b) de la
    cat des Q_p-faisceaux sereins sur X^_K"
  p.8 "... et une équivalence φ_X: P ≅ Q de telle façon que pour M ∈ Mot(X^) φ(Cris_DR-F(M)) ≃ T_p(M)
    {fonctoriel en M, comp. avec les images inverses}". Then: "Soit X de type fini sur Z, intègre, dominant Z,
    lisse pour simplifier. M motif serein sur X ... a) DR(M_Q) Module stratifié et filtré b) ∀p,
    X_p = X⊗_Z F_p, Cris(M|X_p) = M_(p) module stratifié sur X^(p)_Q avec F_p c) Oubliant F_p,
    M_(p) = π_p^*(M) (respectant stratification). Appelons de tels [..] des F_*-coeff. de De Rham, ça fait une
    catégorie." Boxed: "Conjecture (de Groth.) Le foncteur M(X) → ... est pleinement fidèle".
  p.9 "Conj de Tate": Mot(X)⊗Q_ℓ → T_ℓ(X) "pl. fidèle"; then "Conj. de Tate [word unclear]": "X connexe,
    M, N sereins, T_ℓ(M) →u T_ℓ(N): u motivique <=> u_x l'est" (= l-adic VARIATIONAL Tate).
  p.10 "Conj. de Tate [same word] locale": "A anneau local complet pour top. (p)-adique, intègre.
    Mot ser(A) → DR-F-cris(A). Hom_mot(M,N) → Hom_DR-F(cris(M), cris(N)) injectif après ⊗ Q_p; image est
    formée des hom de cristaux qui, après oubli de DR, proviennent d'un hom M_k → N_k (champ résiduel)"
    (= p-adic VARIATIONAL HODGE conjecture, in Hom-of-motives form). Then "Question [struck: Conj.] du double
    réseau: Conj. de Hodge renforcée en oubliant filtration (cas serein)".
- READ BY ME (pp.1, 6): p.1 "Motifs" plan: "Systèmes de coefficients {I définitions, formulaire etc /
  II systèmes de coefficients particuliers / III ? / IV Catégories de motifs}"; base S0 in (Z, Z_(pZ), F_p, Q,
  C, R); T fibred category, T_X triangulated + T°_X abelian (with "troncature ?"); "Yoga 1: On veut
  formalisme RHom, Rf_*, Rf_!, Rf^! (Lf^*)" (six operations). p.6 "Relations entre T_cris et T_DR": X smooth
  over a mixed-char dvr V (perfect residue field), X0 <- X <- X^, X^_K; for a motif M on X: "1°) Cris(M|X0)
  Module loc. libre stratifié sur X^_K (rigide-anal.)" [= a convergent isocrystal on the rigid generic
  fibre; cf. Ogus 1984, Berthelot]; "2°) DR(M|X_K) Module stratifié filtré sur X_K; après oubli de la
  filtration, son image inverse dans X^_K 'est' (1°)" [= crystalline-de Rham comparison, cf. Berthelot-Ogus
  1983]; "D'où suggestion de structure mixte: DR-cristal sur X. D'où DR-F-cristal. M(X) -> DR-F-cristaux".
  => the whole p-adic Hodge set-up (filtered F-isocrystals as realization of motives over a p-adic base)
  is laid out in Grothendieck's hand; pp.7-10 then state the conjectures above.
- Literature (checked by API reads of the papers, quotes): Bloch-Esnault-Kerz, Invent. 2014 (arXiv 1203.2776)
  §1: "A p-adic analog of Conjecture 1.1 is suggested by Fontaine-Messing, it is usually called the p-adic
  variational Hodge conjecture." and "there is no analog of the absolute Hodge conjecture available over p-adic
  fields, which would comprise the p-adic variational Hodge conjecture. So its origin is more mysterious".
  Morrow (arXiv 1408.6783): credits Grothendieck only for the published 1966 VHC; no unpublished notes.
  Published "Motifs" transcription (Elbaz-Vincent/Malgoire 2002; CSG 2024 + 2026 versions): NONE of these
  passages; its §19 "Relation avec la théorie de Hodge" = "[[manque]]", note: "semble avoir été reconsidérer et
  traiter dans le document ..." -> U121 may be (part of) that missing document.
  Web searches (extended): nothing on "Mystère de Tate-Hodge-DeRham", "double réseau", "motif serein".
  Illusie, "Grothendieck at Pisa: crystals and Barsotti-Tate groups" (authoritative history of G.'s 1966-70
  crystalline work; imo.universite-paris-saclay.fr/~luc.illusie/Illusie-Pisa5.pdf), read via API: NO mention
  of any Grothendieck notes on motives + crystals/de Rham; NO motivic full-faithfulness or variational
  conjecture attributed to him. Sources it lists: letters to Tate (5/1966), Illusie (12/1969), Barsotti
  (5/1970), IHES crystals seminar (12/1966, Coates-Jussila notes), Nice ICM 1970, Collège de France 1970-71.
  Mysterious functor stated for BT groups (full faithfulness of G -> (M,Fil)) and "analogues ... in higher
  degrees" (p.18) -> U121's motivic/relative versions go beyond what Illusie records.
- MATH-VALUE CHECK (2026-11-03, maintainer asked "does it actually help math"): my own analysis + an independent
  API analysis agree: (a) p.8 "Conjecture (de Groth.)" = relative (over X/Z, all p, with filtration) form of
  OGUS'S CONJECTURE (LNM 900, 1982: absolute Tate cycles = Hodge cycles; Tang's paper: no Grothendieck credit,
  no relative version in the literature) + Hodge; it REDUCES to Ogus + Hodge + principle B / VHC (specialize
  to closed points, propagate) -> repackaging, not new math. (b) p.8 does NOT imply p.10; p.10 just STATES
  the p-adic VHC (Fontaine-Messing 1987). (c) Nothing on these pages supplies the "absolute Hodge analog over
  p-adic fields" that BEK say is missing -> MY EARLIER "missing framework" READING WAS WRONG (over-interpreted).
  (d) "double réseau" ~ de Rham-Betti algebraicity (consequence of Grothendieck's own period conjecture).
  Mathematical novelty ~2/10. VALUE = HISTORICAL: if dated c.1966-70, Grothendieck stated Ogus's conjecture
  (~15 yrs early) and the p-adic VHC (~20 yrs early) + variational Tate. Revised size: ~6/10 (history of
  arithmetic geometry); the "8" scenario is ruled out.
- (superseded) Meaning (interpretation, needs expert): Grothendieck's own pencil notes (>= 1966: crystals) state the p-adic
  variational Hodge conjecture ~20 yrs before Fontaine-Messing (1987), the l-adic variational Tate conjecture,
  and a global full-faithfulness conjecture (motives over X/Z -> "F_*-coefficients de De Rham") of the kind BEK
  say is missing ("would comprise" p-adic VHC). Also a relative "mysterious functor" (Fontaine-Messing/Faltings).
- Caveats: date uncertain (CSG "ca. 1966"; could be up to ~1970+); provenance unknown; experts close to
  Grothendieck (Illusie, Berthelot, Messing) may know it orally; CSG has had the scan since Nov 2025.
- Size if confirmed: origin of a named OPEN conjecture + the missing framework, in Grothendieck's hand.
  ~6-7/10 in arithmetic geometry (live research area); ~3/10 public. Experts to ask (maintainers decide): Hélène
  Esnault, Matthew Morrow, Luc Illusie, Yves André; CSG/Mateo Carmona for provenance & date.

### L-011 · CANDIDATE (READ BY ME; novelty check in progress) · Gauss: "tangent Graeffe" (root-squaring with derivative)
- Math.20 fol. 3r: https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3381608:00000007/full/1600,/0/default.jpg
- READ BY ME from the image: row 1 coefficients of x^7+3x^4+6; row 2 labelled "D": +7 0 0 +12 0 0 0 =
  the DERIVATIVE 7x^6+12x^3. Both rows carried together through root-squaring steps (main + "D" rows
  each step); log columns of root moduli (some marked "n" = negative). Bottom:
  "(x - a^64 - a^63 w)(x - b^64 - b^63 w)(...) = X + Y w" and "a^63/(x-a^64) + b^63/(x-b^64) [+...] = Y/X".
  => f + w f' (dual number / infinitesimal shift) pushed through 6 squarings; a^63 recovered next to a^64,
  so a = a^64/a^63 gives the root itself (sign/argument), not just its modulus.
- Modern: "tangent Graeffe" iteration (Malajovich-Zubelli 1999, arXiv math/9908150; used in modern
  computer algebra). Usual credit: idea traced to Brodetsky & Smeal 1924 (origin shift, "ad hoc").
  Root-squaring itself: Dandelin 1826, Lobachevsky 1834, Graeffe 1837; Encke 1841 (complex roots).
- Novelty so far: 2 web searches - nothing crediting Gauss. TO CHECK: Householder 1959 (AMM, history),
  Ostrowski 1940 (Acta Math 72, Graeffe), Encke 1841 (does Encke use a derivative row?), Gauss-Encke
  correspondence; Lemmermeyer; dating of Math.20 (neighbours name Harding/Bessel/Olbers).
- Size if true: anticipation of a named technique still used today, >= ~70 yrs before Brodetsky-Smeal.
  Smaller than L-006 (numerical-method detail, Graeffe base method not his). ~5/10 in history of math.

### L-010 · PARKED (medium; novelty search clean, not hand-verified) · Gauss: binary Hermitian forms over Z[i]
- Math.5 fol. [24v]: image https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3376170:00000050/full/1300,/0/default.jpg
- Deep reader: transformation/neighbouring forms of a xx' + b xy' + b' x'y + c yy' (conjugate variables),
  proper vs improper equivalence, a worked Gaussian-integer continued fraction, 83 = 3^2+5^2+7^2 via norms.
  Usually credited: Hermite 1854 (Hermitian forms), Picard/Bianchi 1880s-90s (forms over Z[i]).
- Novelty: web search found nothing crediting Gauss; Werke II/III/V no match. To check: Goldstein, "The
  Hermitian form of reading the Disquisitiones" (in The Shaping of Arithmetic, 2007); Lemmermeyer.
- Size: medium (undated; not a major theorem). Not verified by me yet.

### L-009 · PARKED (medium; novelty search clean, not hand-verified) · Gauss: Sturmian words with arbitrary intercept
- Math.5 fol. 15r: image https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3376170:00000031/full/1300,/0/default.jpg
- Deep reader: differences of floor(A + j p) built from continued-fraction blocks (homogeneous case =
  Johann Bernoulli III 1772, stated without proof); Gauss treats general intercept A by expanding frac(A)
  against the continued-fraction remainders (Ostrowski-type) and states the inverse problem.
  Usually credited: Christoffel 1875, Smith 1876, Markov 1882, Ostrowski 1922, Morse-Hedlund 1940.
- Novelty: web search found nothing crediting Gauss; Werke II/III/V no match.
- Size: medium (combinatorics-on-words priority detail). Not verified by me yet.

### L-008 · DUPLICATE (core finding published 2025) · Gauss computing 10-adic logarithms
- **Where:** Gauss, Cod. Ms. Gauss Math. 21 ("Varia Arithmetica"), fol. 16r, 16v, 17r, 37r.
  17r: https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3381609:00000033/full/1600,/0/default.jpg
- **Verified (READ BY ME + exact recomputation, targets/gauss/verify/l008_decadic_log.py):** 10-adic logs
  mod 10^17 written on 17r: log 11 = 24 28814 27506 84460 (=Lambda 11), Lambda 9 = 60 16168 85573 10440,
  log 51 = 67 29433 33943 11300, log 49 = 04 31047 91025 61200, log 21 = 82 23608 38299 35820,
  log 19 = 05 87919 50819 83780 -> 6/6 EXACT. Halving ambiguity written as stacked leading digits
  (30|80, 52|02, 37|87) = exactly the 2 correct candidates. Gauss slip: log 17 written "37 26348 91156
  56080", correct 37 21348 ... (one digit). Also on 16r: 10-adic inverses (1/3=...6667), idempotents
  (...90625/...09376), torsion splitting with eps (eps^4=1), decadic exponential ("Numerus cuius L=20").
- **Prior work:** F. Lemmermeyer, "Gauss and p-adic numbers", arXiv 2510.11559 (13 Oct 2025): Gauss's
  "infinite congruences" = p-adic numbers; 10-adic square root of 1; 10-adic logs of small integers by
  power series; 11-adic sqrt 5. His sources: Cod. Ms. Gauss Schedae 5 ("Varia", July 1800) and
  "Mathematische Brouillons, Oktober 1805" (DE-611-HS-3376629 = our Math.11). Also Frei (Gauss had
  Hensel's lemma), K. Conrad's Hensel's Lemma notes. => core claim KNOWN. Our pipeline independently
  rediscovered it (validates the method).
- **Possible small addendum (unverified as new):** Math.21 is a different manuscript with more extensive
  work (17 digits, eps-splitting, exp, index table mod 10^8 via the log on 37r). Could be offered to
  Lemmermeyer as additional material - maintainer's decision. Not a lead under rule 9.

### L-007 · CHECKED 5/10 by independent check (2026-11-03); FROZEN under rule 9b
- Not found published. Related published material: Werke VIII pp.21-26 (Gauss's cube-root integers, unit for
  n=2; no series); diary entry 137 (23 Dec 1808: "Theoriam formarum cubicarum, solutionem aequationis
  x^3+ny^3+nnz^3-3nxyz=1 aggressus sum", Werke X.1 p.568); Bachmann X.2 §25 (no series). Dirichlet 1841,
  Eisenstein 1844: units, no L-series. Dedekind (Crelle 121, 1900; draft 1871/72): credits Gauss with the
  arithmetic half ("im Wesentlichen schon Gauss bekannt"). Note = natural extension of Gauss's own quadratic
  class-number formulas (1800, Werke II p.285). NUMERIC: the series as written converges to ~1.2971 vs
  L(1,chi) ~0.8146 for Q(cbrt2) -> related but not exactly the right L-series. If c.1808: earliest statement
  linking a cubic unit to an L-type series (~65 yrs before Dedekind). One line, undated -> 5/10.
### (old header) L-007 · CANDIDATE (moderate; one-line idea; DUPLICATE RISK RAISED)
- **Risk note (loop G-8):** Lemmermeyer (arXiv 2510.11559) cites "Mathematische Brouillons, Oktober
  1805" = DE-611-HS-3376629 = the same bundle (Math.11) that contains this note; he is also the leading
  historian of cubic/higher reciprocity. His p-adic preprint text does not mention the cubic-form/series
  note, but check his other work (Reciprocity Laws book; papers on Gauss's cubic forms) before claiming. · Gauss links units of Q(cuberoot 2) to a cubic L-series
- **Where:** Gauss, Cod. Ms. Gauss Math. 28? NO -> Math. 11 ("Kubische Reste"), folio 15r, top note.
  Image: https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3376629:00000027/full/1300,/0/default.jpg
- **Verbatim (read by me from the image):** "Solutio aequationis x^3 + 2y^3 + 4z^3 - 6xyz cohaerere debet
  cum summatione seriei Sum eps^n/(mm+3nn)" (z exponent overwritten; norm form needs z^3).
- **Meaning (my check):** x^3+2y^3+4z^3-6xyz = norm form of Q(2^(1/3)); its solutions of value 1 = units
  (fundamental unit 1+theta+theta^2). eps^n with eps a cube root of unity, over m^2+3n^2, matches the
  cubic residue character of 2 (2 is a cubic residue of p iff p = x^2+27y^2, i.e. 3|n). So: units of a
  pure cubic field tied to a cubic L-series = idea of the analytic class number formula for pure cubic
  fields (zeta_K = zeta * L(chi) * L(chi-bar)).
- **Usual credit:** Dirichlet (1840s, cubic forms/units), Eisenstein (1844), Dedekind (1900, class number
  of pure cubic fields).
- **Prior work checked:** Bachmann (Werke X.2 Abh.1): knows Gauss used the cubic form x^3+ny^3+n^2z^3-3nxyz
  (Handbuch 18, Oct 1805, note on "duplicierte quadratische Formen") and knows Gauss's quadratic
  class-number formula (Werke II p.285) - but NO mention of linking the cubic form's units to a series.
  Not checked: Werke VIII / X.1 (blocked), Lemmermeyer's histories of reciprocity / cubic fields.
- **Size (honest):** one-line expectation, no computation; a nice footnote if unknown (~4-5/10 history).
- **Bottom of same page** (biquadratic supplementary laws, Gauss marks own formula false at 5+4i): known
  material (Gauss 1832; Eisenstein 1844) -> not a lead.

### L-006 · DOWNGRADED to ~4/10 by independent check (2026-11-03); FROZEN under rule 9b
- COUNTER-EXAMPLE TO "first 3-D before Kronecker": HERMITE, C. R. 35 (1852) "Sur l'extension du théorème de
  M. Sturm à un système d'équations simultanées": counts common real roots of 2 equations in a rectangle via
  corner sign-variation counts n = (A-B+C-D)/2 and says the analogy "se maintient encore lorsque l'on considère
  trois équations simultanées", count inside a "parallélépipède droit"; full memoir (12 Jul 1852, Oeuvres III
  1912) works a 3-variable example, claims any number of equations. (Algebraic/Sturm-type, exact count, vs
  Gauss's continuous functions + Jacobian signs = Kronecker-like structure.) All earlier checks (ours + the
  maintainer's other session) MISSED Hermite 1852. Dating risk: bundle runs to 1853 -> Gauss could post-date Hermite.
  Known Gauss links to degree theory: FTA winding (Mawhin), Kronecker 1869 cites Gauss's potential-theory
  "Allgemeine Lehrsätze" (Werke V p.225), 1833 linking number (Epple). Rating ~4 (up to ~5 if dated < 1852):
  short Historia Mathematica note at most.
### (old header) L-006 · STRONG CANDIDATE (prior-work check mostly done; holes: Siegberg, Epple, hand/date) · Gauss: degree/index theory for systems of 2 and 3 equations on a box
- **Where:** Gauss, Cod. Ms. Gauss Math. 28 ("Varia Analytica"), folio 7r-7v (canvases 14-15).
  7r: https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3381843:00000015/full/1600,/0/default.jpg
  7v: https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3381843:00000016/full/1600,/0/default.jpg
  (verify canvas->image mapping via targets/gauss/pages/Math.28/manifest.json; local copies g28_c014/015.jpg)
- **Verbatim (READ BY ME from the images; matches machine transcription):** heading "Verschwindende
  Werthe einer, gleichzeitig verschwindende mehrerer veraenderlichen Groessen". II: boundary sign-count
  rule for y, y' on rectangle; "Das Resultat dieser Zusammenzaehlungen sei +-4m. Es wird dann allemahl m
  eine ganze Zahl sein, und man kann behaupten dass wenn nicht m = 0 wird, sich gewiss innerhalb jener
  Grenzen wenigstens Eine Combination von Werthen fuer x und x' findet wofuer zugleich y = 0 und y' = 0.
  Man kann sogar noch weiter gehen." Multiplicity: "lambda' + 2 lambda'' + 3 lambda''' u.s.w. nicht kleiner
  als m ... so kann man behaupten dass es wenigstens m Aufloesungen innerhalb jener Grenzen giebt."
  III: "Fuer den Fall dreier veraenderlicher Groessen x, x', x'' ... kann ... die Nothwendigkeit eines
  gleichzeitigen Verschwindens auf aehnliche Art aus dem Verhalten auf den Grenzen erkannt werden" with
  rule: on faces, points where two functions vanish, sign of 2x2 Jacobian
  (dy/dx')(dy'/dx'') - (dy/dx'')(dy'/dx') = +-eps(1,2;0,1) times sign of third function; cyclic index
  orders 1,2 / 2,0 / 0,1; "fuer jedes positive eps ... +1, fuer jedes negative -1".
  ("In analytischer Einkleidung" replaces a struck "geometrischer"; a struck geometric description of the
  box as region between 6 pairwise parallel planes.)
- **Modern meaning:** boundary formula for the topological (Brouwer/Kronecker) degree of maps R^2->R^2
  and R^3->R^3 on boxes; integrality; nonzero degree => a zero exists (Poincare-Miranda / Kronecker
  existence); #zeros counted with multiplicity >= |degree|. III = Kronecker-type recursive boundary
  count (2D Jacobian sign on faces x sign of third component) - the formula used in computational degree
  methods (Stenger 1975, Kearfott 1979).
- **Usual credit:** Cauchy indices (1831/37) and Sturm (1836) for 2D counting; Kronecker 1869
  (characteristic, n-dim); Poincare 1883/86 + Miranda 1940 (box existence); Brouwer 1912 (degree).
- **Prior-work check so far (NOT in):** web + extended search; Werke II, III (has only the published 1849
  FTA paper), V; Staeckel "Gauss als Geometer" (Werke X.2 Abh.4) - discusses Gauss's Geometria situs,
  knots (Werke VIII 271-285), 1833 linking integral as "erste Anfang" of Kronecker's characteristic theory,
  FTA proofs - NO mention of this box-counting theory. Degree-theory histories (Mawhin; Dinca-Mawhin
  ch.23) start formal theory with Kronecker 1869; Siegberg 1981 (AMM 88) traces "from Gauss via Kronecker
  to Brouwer" - contents unchecked (paywall). Blocked: HathiTrust (403), GDZ search (HTTP 500).
- **Mathematical verification (2D):** targets/gauss/verify/l006_rule2d.py implements Gauss's fol. 7r
  rule LITERALLY (factors (i)-(iv); negative sides x=-a and x'=+a' as he names them). 12/12 test maps
  (complex polynomials incl. double root, roots inside/outside, orientation-reversing conj maps, 6
  random): S = -4 x (signed zero count inside, with multiplicity) EXACTLY. So his rule computes the
  topological degree; claims (a) integrality, (b) m!=0 => zero, (c) count with multiplicity >= |m|
  all hold. (One initial mismatch was MY sampling bug: exact zeros at grid points; fixed.)
- **Mathematical verification (3D):** targets/gauss/verify/l006_rule3d.py implements the fol. 7v rule
  literally (faces x_i=s, face coords cyclic (i+1,i+2), function pairs (1,2),(2,0),(0,1), eps = s *
  sign(third fn) * sign(2x2 Jacobian)). 14/14 random quadratic maps R^3->R^3 (degrees -2,-1,0,1;
  incl. degree-0 maps with 2 cancelling zeros): T = 6 x degree EXACTLY. => Gauss's 3-D rule is the
  Kronecker-type boundary formula for the Brouwer degree (6 = 3 pairs x 2 signs). Fragment ends on
  7v (8r = show-through only; 8v = unrelated lemma on derivatives). No proofs, no date on the sheet.
- **Dating (loop G-6):** sheet undated. Neighbouring Math.28 folios carry dates 1821-1853 (fol.10v 1821;
  13v/14r receipt 4 Oct 1825; 26r Jacobi 1846; 32r pi-computers 1853) - bundle not chronological.
  "Einkleidung" (sheet: "In analytischer [struck: geometrischer] Einkleidung") is a Gauss idiom in BOTH
  his 1828 Descartes-rule paper and the 1849 4th FTA proof (Werke III) -> not decisive. Bound: before
  Gauss's death (1855) => >= 14 years before Kronecker 1869.
- **Gauss never published it:** the 1849 FTA paper (Werke III) has no several-variable / box / simultaneous-
  vanishing theory (grep: no hits) -> the 2D/3D box degree theory exists only on this sheet.
- **More prior-work facts (zbMATH/JFM):** Werke VIII (1900; analysis ed. Fricke, geometry incl.
  Geometria situs ed. Staeckel) = "einzelne Notizen und Aufsaetze ... aus dem Nachlass"; X.2 essays:
  Bachmann, Schlesinger (function theory, 222 pp., uses manuscripts; review mentions conformal maps,
  AGM, elliptic fns, Cauchy's theorem before Cauchy - not degree/box counting), Ostrowski (1st & 4th
  FTA proofs), Staeckel, Bolza, Maennchen, Geppert. Blocked: TIB goobi viewer (bot wall; it holds a
  Werke vol. with "ANALYSIS. NACHTRAEGE ZU DEN BAENDEN III UND VIII", record 897683412), Google Books
  API (HTTP 429 anonymous quota - retry later), HathiTrust 403, GDZ search 500.
- **External prior-work evidence (project rule):**
  - Mawhin, "Poincare's early use of Analysis situs in nonlinear differential equations", Philosophia
    Scientiae 4(1) (2000) 103-143: Gauss mentioned only via Johnson (1981) quote (index implicit in FTA
    proofs 1/3/4); p.115 calls Poincare's 1884 statement "the first occurence" of the n-dimensional
    intermediate value theorem -> Mawhin knew of no earlier Gauss statement (as of 2000).
  - Dinca & Mawhin, Brouwer Degree (2021) ch.1 bibliography: cites Gauss 1799, 1816 FTA proofs (Werke III
    1-55, 59-64) and 1833 note (Werke V 605) - not this manuscript.
  - Sturm, JMPA 1 (1836) 290-308: two variables only (contour; rectangles), no "trois".
  - Sturm & Liouville, C.R. 4 (1837) 720-724: their analysis "aux racines reelles des equations a deux
    inconnues"; call Cauchy's general proposition inexact.
  - Cauchy, C.R. 4 (1837) 672-674 (8 May 1837 letter, Turin lithograph 1833): READ BY ME (archive.org
    comptesrendusheb04scie): "Huitieme theoreme" = two functions f(x,y), F(x,y) on rectangle ABCD,
    claims 2N = boundary index sum (N = number of solutions) -> 2D only; Gauss's sheet states the
    CORRECT inequality form ("wenigstens m Aufloesungen").
  - Werke VIII sections: Analysis u. Functionentheorie pp.33-118; Geometria Situs pp.269-286 (individual
    titles not yet seen). Werke X.1: structure only.
  - Still open (being checked by the maintainer's other session; do NOT duplicate unless asked): Cauchy
    "Calcul des indices" (J. Ec. Polyt. 1837) for 3 variables; Werke VIII/X.1 piece titles; Siegberg 1981.
  - UPDATE 2026-11-02 (project rule):
    - Siegberg 1981: article text NOT readable (paywall). Works citing it cite it only for Kronecker's
      integral / Cauchy / Picard; none links it to Gauss or Math.28. Mawhin, Adv. Nonlinear Stud. 4 (2004)
      p.535: Cauchy's index "implicit in some of Gauss' proofs of the fundamental theorem of algebra"
      (no citation) -> refers to the published FTA proofs, not this sheet. OPEN (needs library access).
    - Cauchy "Calcul des indices" (Oeuvres ser.2 t.1 pp.416-466): text NOT obtained (Lille copy bot-walled;
      fetchable copy stops ~p.51). Secondary sources ALL describe Cauchy as 2-D: Cayley, Trans. Camb. Phil.
      Soc. 12 (1877) 395-413 ("two-curve theorem", P=0, Q=0 in a plane); Johnson 1981 via Mawhin 2000
      pp.109-110 ("Kronecker (1869) generalised Cauchy's index from two to n dimensions"); Poincare 1883
      via Mawhin p.113 (credits n equations to Kronecker). Cauchy's 3 July 1837 note and 1855 papers
      unchecked. OPEN: one primary read of pp.416-466 closes it (Gallica scan, linked from Mathdoc).
    - Werke VIII/X.1 piece titles: still running there.
  - UPDATE 2 (project rule):
    - Cauchy "Calcul des indices" (Oeuvres ser.2 t.1 pp.416-466, archive.org scan, n = page+13): TWO
      variables only. p.432 Thm VIII: f(x,y), F(x,y) on x0..X, y0..Y, N = 1/2 sum of 4 side integrals;
      p.433 Lemme I plane coords; p.466 formula (73) = rectangle case = end of 1833 Turin memoir. Text
      search: no z, no "trois inconnues", no parallelepiped/surface/volume. Only triple = "u, v, w trois
      fonctions de x, y" (3 functions of 2 variables).
    - Cauchy 3 July 1837 note (C.R. t.5 p.6; Oeuvres ser.1 t.4 pp.81-83): two variables; p.83 admits Thm
      VIII "peut devenir inexact" (exact count fails) -> Gauss's sheet has the CORRECT form ("wenigstens m").
      Caveat: Oeuvres reprint omits part of the C.R. text (rows of dots on p.82).
    - Werke VIII (Analysis pp.33-118: 13 pieces listed; Geometria situs pp.269-286: knot/curve notes,
      p.281 point-in-figure test) and X.1 (Algebra 99-136, Analysis 137-450, Geometrie 451-482): NOTHING
      matching; text search no "Verschwindende Werthe"/"gleichzeitig verschwindende". Sheet unpublished.
    - Siegberg 1981: still unreadable.
  - NET STATUS (after update 2): STRONG. Primary texts of Cauchy (1833/1837) and Sturm (1836) = 2-D only;
    Werke does not print the sheet; histories credit n-D to Kronecker 1869. Remaining holes: (1) Siegberg
    1981 text; (2) Moritz Epple's studies of Gauss's topological Nachlass ("Die Entstehung der
    Knotentheorie" 1999; "Orbits of asteroids, a braid, and the first link invariant", Math. Intelligencer
    1998) - he worked through Gauss's Geometria-situs manuscripts and may have seen Math.28; (3) expert
    confirmation that the hand is Gauss's + dating; (4) Vergnerie, Rev. Hist. Math. 25(1) 2019 on
    Kronecker's theory of characteristics (numdam, PDF - not read) - check its precursor section for
    Gauss. Web search (Epple + Gauss + Kronecker + simultaneous zeros): nothing linking Gauss to a box
    rule; Dyck 1895 links Gauss's LINKING integral (published 1833 note) to Kronecker's characteristic -
    that is a different, known connection. Best expert: Epple (Frankfurt) or Mawhin.
  - UPDATE 3 (project rule): Vergnerie RHM 25(1) 2019 pp.1-107 full text: no "verschwind",
    "Math. 28", "Cod. Ms"; manuscript/Nachlass hits = Kronecker's own notes only; Gauss cited 72x only for
    published FTA proofs (1799/1816/1849); bibliography: Werke III only. Epple, "Geometric Aspects in the
    Development of Knot Theory" (History of Topology, 1999) ch.11 full text: Gauss Nachlass = knots,
    Tractfiguren (1825/1844), braid page, linking number - no systems of equations/index/Cauchy.
    Unread: Epple's book Die Entstehung der Knotentheorie (1999; MathSciNet review lists only knot topics),
    Epple 1998 Math. Intelligencer, Siegberg 1981. => holes left: Epple book + Siegberg (library), hand/date.
  - (superseded) NET STATUS: every source read (primary 2-D texts + 3 independent historical summaries) puts the first
    beyond-2-variable version at Kronecker 1869. No source mentions this sheet. Remaining holes: Cauchy
    pp.416-466 primary text, Werke VIII/X.1 titles, Siegberg 1981 text.
- **Still to check:** Werke VIII (1900) and X.1 (1917) contents (try JFM reviews via zbMATH API, GDZ
  later); Schlesinger (Werke X.2 Abh.2) and Ostrowski (X.2 Abh.3, on 1st/4th FTA proofs); Siegberg 1981 (text);
  dating of the sheet (handwriting, neighbouring folios; relation to 1849 FTA paper).
- **Size if unrecognised (interpretation):** history-of-math "how did we miss this": Gauss stating a
  degree/index existence-and-counting theory in 2D and 3D decades before Kronecker (1869) and Poincare
  (1883). Not new mathematics today, but a notable correction to the history of topology. ~7/10 within
  history of math. Expert to ask: Jean Mawhin (historian of degree theory) - maintainer sends, not me.

> PRIOR-WORK CAVEAT (all Hilbert leads): the diary is known to historians (Springer Hilbert
> Lectures vol. 6, selection of foundational notebook material, now listed Jun 2030; Hayashi
> "Hilbert Notebook Project" ~2006). Our entries are technical, likely outside vol. 6's
> scope, but the ENTRY may be known to these historians. The MATH was checked separately:
> zbMATH Open + web, nothing solving L-003/L-004 found.

### L-005 · OPEN (novelty unverified; size MEDIUM-SMALL) · Are Riemann maps of algebraic-oval domains differentially algebraic?
- **Where:** Hilbert 600/2 (1892-1900), p. 1 (canvas 6). Machine transcription (TODO re-read):
  "zu dem Problem zu beweisen, dass jede Function welche das Innere eines Ovals einer
  algebraischen Curve auf eine Halbebene abbildet einer gewoehnlichen algebraischen
  Differentialgleichung genuegt."
- **Plain English:** Hilbert wanted to PROVE that the conformal map of the inside of any
  algebraic oval onto a half-plane satisfies an algebraic ODE (is differentially algebraic).
- **Known:** true for polygons (Schwarz-Christoffel), circular-arc polygons, ellipse (elliptic
  functions). Hypertranscendence theory is active (Hardouin et al.; arXiv 2508.14645 on
  transcendence of uniformization maps, 2025 - related, different question).
- **Hilbert's own conclusion (page text):** Lindemann's approach (curve in z, z') "fuehrt aber
  nur in dem ganz besondern Falle, dass phi(z,z') = z^n + z'^n + 1 [?] ist" -> special case only;
  he then moves on. Never returned (no other diary entry found).
- **Prior work trail (special shapes only):** Schwarz 1869 (ellipse, parabola); Lindemann
  1890/97 (hyperbola) and 1894 Munich Acad. "Ueber die conforme Abbildung der Halbebene auf ein
  einfach zusammenhaengendes Flaechenstueck, das von einer algebraischen Curve begrenzt wird"
  (publikationen.badw.de/en/003392735/003392735.pdf); Goettler 1900 (circular cubic, bicircular
  quartic; method works only "if a suitable rational function can be found"); Bonder 1951
  (exteriors of arcs, eudml.org/doc/11713); quadrature domains: Aharonov-Shapiro 1976,
  Gustafsson, Bell (map algebraic). NONE found answering the GENERAL question or stating it open.
- **Novelty check:** triage (none) + my extended search (none addresses it). My expectation
  (interpretation): false in general (e.g. quartic oval x^4+y^4=1), but no proof known to me.
- **Size (honest):** a solid research question in complex analysis / differential algebra;
  resolving it = a good paper, not a breakthrough.

### L-004 · OPEN (novelty unverified) · Hilbert's real-roots claim for powered binomial polynomials — FALSE as stated; true threshold unknown
- **Where:** Hilbert 600/2 (1892-1900), p. [48] (canvas 53).
- **Verbatim (machine transcription; TODO re-read image):** "Beweise dass die Gleichung
  x^n + (n 1)^alpha x^{n-1} + (n 2)^alpha x^{n-2} + ... + 1 = 0 fuer alpha > 1 lauter reelle,
  fuer alpha < 1 lauter imaginaere Wurzeln hat. ausser einer fuer ungerades n."
- **Plain English:** Hilbert claims P_{n,a}(x) = sum_k C(n,k)^a x^k has ONLY REAL roots when
  a > 1 and NO real roots when a < 1 (except the forced root -1 for odd n).
- **Our computation (60-80 digit mpmath, targets/hilbert/verify/s016_powered_binomial.py):**
  (a) FALSE: for a = 1.01..1.1 every even n >= 4 has non-real roots. True cutoff a*(n)
  (bisection): n=4 1.1477, 6 1.2013, 8 1.2431, 10 1.2795, 12 1.3203, 16 1.3752, 20 1.4102,
  24 1.4461, 26 1.4599 (rising). a = 1.5 FAILS for n = 40, 50, 60 (24/40, 22/50, 24/60 real);
  a = 1.7, 1.9, 2.0, 2.5 real-rooted for all n tested up to 60.
  (b) holds numerically: no violations for n = 2..20, a in {-3,-1,-0.5,0,.25,.5,.75,.9,.99}.
- **Open questions it raises:** (1) limit a* = lim a*(n) (somewhere in (1.5, 1.7]?);
  (2) is a* the Laguerre-Polya threshold of the entire function sum z^k/(k!)^a (order 1/a),
  i.e. the smallest a for which (1/(k!)^a) is a Polya frequency sequence? (3) prove (b).
- **Why it might matter (interpretation):** real-rootedness / Laguerre-Polya / multiplier
  sequences are an active area (Vishnyakova, Nguyen, Kostov 2019-2023; Branden). A clean
  "Hilbert's claim is false; here is the true threshold" note is publishable-sized. Modest
  scientific size, but concrete, checkable, with new data.
- **Novelty check:** triage web search (none); my extended search on both the binomial family
  and sum z^k/(k!)^a (none settles it; related LP-class literature found). Not checked:
  zbMATH, Polya-Szego problem books, Craven-Csordas papers. NOT verified new.
- **Writer-identification classifier (2026-11-09; src/writer_id.py, docs/WRITER_ID_RESULTS.md in the public repo):** RootSIFT at ink keypoints → codebook → logistic regression, trained on 164 pages of known hand (Riemann 59: dated letters, "Italien" notes 1862/65, 1857 drafts; Weierstraß 4; Weber 11; Dedekind 30; Hilbert 30; Gauss 30), 5-fold CV grouped by page: six-class accuracy 97.6 %, binary Riemann-vs-not 98.2 %; Riemann pencil pages 10/10. Targets never trained on: fol. 70v → Riemann 0.998, 71r → 0.978, 19/3v → 0.969; controls: 19/97r (printed by Noether 1902 as Riemann's) → Riemann 0.999, 19/101r (Weierstraß) → Weierstraß 0.975. Limits: closed set of six hands (cannot reject an unknown seventh writer), same-volume scan confound, thin Weierstraß class. This is measured evidence for the hand; it does not replace a palaeographer, but the question is now "is there a seventh writer in these volumes?", not "is it Weber or Weierstraß?".
- **Next:** re-read page image to confirm transcription; compute a*(n) to n~100 in background;
  test LP property of sum z^k/(k!)^a directly; targeted search Craven-Csordas / Katkova-Vishnyakova.

### L-003 · OPEN (novelty unverified; needs expert check) · Hilbert's generalised Gordan problem
- **Where:** Hilbert, Cod. Ms. D. Hilbert 600/1 (research diary 1886-1892), p. 3 (canvas 12).
  Scan: https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3763733:00000013/full/1500,/0/default.jpg
  (verify index via targets/hilbert/pages/600_1/manifest.json canvas 12). Page = an early
  problem list (7 short tasks separated by rules).
- **Verbatim (read by me from the image, matches machine transcription):** "Verallgemeinerung
  des Gordanschen Problems eine Form 6ten Grades als Summe eines Quadrates und einer dritten
  Potenz darzustellen: f = phi^m psi^n + chi^sigma rho^mu    f' = phi'^m psi'^n"
- **Plain English:** Gordan/Clebsch asked how a general binary form of degree 6 can be written
  as (quadratic)^3 + (cubic)^2. Hilbert proposes the general problem: write a binary form as a
  sum of TWO PRODUCTS OF POWERS of forms, f = phi^m psi^n + chi^sigma rho^mu (degrees
  matching), with a companion single-product form f' = phi'^m psi'^n.
- **Why it might matter (interpretation):** decompositions of binary forms are an active area:
  sums of powers / Waring problems for forms (Froberg-Ottaviani-Shapiro 2012; Lundqvist-Oneto-
  Reznick-Shapiro; Reznick 2020), A. Patel 2025 "Counting sums of two powers" (arXiv 2507.08337)
  generalises exactly the Clebsch cube+square count to g^a + h^b, but not to products. Coincident
  root loci (products of powers of LINEAR forms) and their joins are studied (Chipalkatti;
  Feher-Nemethi-Rimanyi; Lee-Sturmfels duality). Hilbert's version with arbitrary-degree
  factors = joins of "power-product" varieties; perfectly-dimensioned cases should give finite
  decomposition counts -> concrete enumerative problems.
- **Novelty check:** (1) triage agent (web search): none found, low confidence, search cut short;
  (2) my extended search "sum of two products of powers ... secant ... coincident root loci":
  none found. Not checked: zbMATH/MathSciNet, 19th-c. Gordan-school literature (Gordan,
  Clebsch, Study, Meyer reports). Status OPEN, NOT verified new.
- **Size (honest):** a niche algebraic-geometry research question, not a famous problem.
- **Next:** (a) enumerate perfectly-dimensioned cases (param count = deg+1) by code;
  (b) for the smallest new case, test numerically whether decompositions exist and count them;
  (c) check Patel 2025 references + Gordan's original papers for any treatment of products.

## Dropped (not big, rule 9)
- (2026-11-08) cote 5 p.50 [5] (typescript, letter of 10.12.1965, Grothendieck-Deligne crystals correspondence):
  conjecture that p-adic étale cohomology over C_p maps Z_p-linearly into de Rham cohomology, iso after ⊗K, via a
  Poincaré lemma on Tate's rigid-analytic space (Hodge-Tate / Fontaine / Scholze lineage). The 1965 Deligne
  correspondence is CSG-transcribed and was read in the CSG letters batch (G-10d) -> DUPLICATE, noted only.
- (2026-11-08) cote 7 p.17 [5] (1966-67 crystals talks): proposes replacing the crystalline site by a site of pro-
  infinitesimal thickenings built from Monsky-Washnitzer weakly complete lifts (Zariski-type topology) to get a p-adic
  cohomology with values in K that inverts p correctly - the idea realised later by Berthelot's rigid cohomology (1986)
  and Le Stum's overconvergent site (2011); topology/cohomology left undefined. Priority sketch; noted only.
- (2026-11-08) cote 13 p.5 [5] (1965): Tannakian polarization criterion - every V ∈ Rep(G) polarizable ⇔ centralizer of
  the Weil operator C = j(i) in Ker(ε)_R is maximal compact (Cartan involution), with G ≅ G' ×_{Z/2} G_m; next page
  families parametrized by G'(R)/K. = Deligne 1971/79 Shimura-datum axiom / Deligne-Milne 1982 polarization prop.
  Transcription only; sent to the cote-15 combined check as cluster D. Expected priority detail.
  Also 13 p.9 [5]: 'G-variations' of Hodge structure on a complex space S (tensor functors Rep(G) → Hodge(S) with
  weight, polarisability, rigidification) classified by monodromy α: π_1(S) → G(Q) + a Π-equivariant period map from
  the universal cover; arithmetic level structures started. (Griffiths 1968-70 / Mumford 1966 / Deligne territory.)
  Also 13 p.15 [5]: English P.S. of a 1965 LETTER (probably to Mumford: 'your θ-fns, are you going to write a book?')
  listing the 'modular varieties' predicted by motivic Galois theory = Shimura-datum axioms in circle-group form
  (i0(−1) central; centralizer of i0(i) maximal compact; nontrivial on each simple factor) + conjecture that all
  such arithmetic quotients are algebraic (false in the non-Hermitian case). LIKELY PUBLISHED in Mumford's Selected
  Papers II (2010, Grothendieck correspondence). CONFIRMED: p.13 = "Dear Mumford", Algiers, Nov 1, 1965 -> the whole
  Grothendieck-Mumford correspondence 1958-86 is published in Mumford's Selected Papers II (2010) -> DUPLICATE. Cluster D
  check (2026-11-08): the p.5 polarization ⇔ Cartan-involution criterion = Saavedra 1972 ch. V / Deligne 1979 / Milne
  "Shimura varieties and moduli" Thm 2.1; Milne 2025 credits the NOTION of polarization to Grothendieck (undated);
  cote 13 notes may be 1967-71 (SGA 7 ref., Bourbaki 383 verso). Rating 4/10. DROPPED.
  Also 13 pp.40-42 [5]: a family of motives over S with group G packaged as (monodromy w: π_1(S(C)) → G(Q), holomorphic
  equivariant period map f into the space of h: S → G_R of fixed weight, adelic/étale factorisation) - the Shimura-
  variety triple; programme left incomplete.
- (2026-11-08) cote 15 p.222 [5] (verso of Bourbaki n° 370, 1964): conjugate varieties with non-isomorphic integral (or
  real?) cohomology RINGS (Serre 1964 / Charles 2009 territory), Betti torsors P_v under G_M over Z or R for different
  embeddings, "Conjecture A" (distinct embeddings give non-isomorphic integral torsors), G_M(Z) as a "true fundamental
  group". Checked (cluster C, 2026-11-08): 5/10 - the question is already credited to Grothendieck ("Montréal, July
  1970") by Charles 2009, who answered it (conjugates with non-isomorphic real cohomology algebras); the torsor form is
  standard bookkeeping; Conjecture A (rational/real form) is thus a theorem now. DROPPED.
- (2026-11-08) cote 15 p.158 [5] (1965): the commutative group scheme classifying abelian motives over a number field K
  = R_{O_K/Z}G_m modulo the Zariski closure of the totally positive units (an integral model of Serre's torus T_m / S_m,
  Serre 1968 McGill lectures). Contemporaneous with Serre, close contact; priority detail only -> noted, not pursued.
  Also p.160 [5]: the same group as an extension 0 → G° (torus) → G → Pic(A)^abs → 0 with Hodge realisations at each
  place (Serre/Taniyama-group shape). Same note.
- (2026-11-07) cote 142 p.94 [5] (1978-): necessary conditions for an automorphism of the profinite fundamental
  groupoid of ONE anabelian variety over a finitely generated K to come from Gal(K̄/K): lifts to every finite étale
  cover fixing K-rational base points + stability of π_1-images under K-maps to hyperbolic curves. = single-variety
  form of the "fundamental conjecture" / I-OM question (public via the 1983 Faltings letter + Esquisse; Ihara,
  Oda-Matsumoto, Pop). Sketchy, upside < 7 -> noted only, not viewed.
- (2026-11-07) Montpellier cote 153 "Analyseurs" p.1 [5] (c.1982): k0-algebra Ω0 with composition F∘G, unit T, right
  composition a ring map, co-addition/co-multiplication, acting on non-unital algebras; model Int(Z) (binomial polynomials).
  Read by me (matches). Deep reader called it an uncredited anticipation of plethories (Borger-Wieland 2005) - WRONG:
  the same structure is Tall-Wraith 1970 ("Representable functors and operations on rings", Proc. LMS 3, 619-643),
  which Borger-Wieland credit; the title word is Lazard's 1955 "analyseurs" (Ann. ENS 72, 299-400; operad precursor).
  Re-derivation of known 1955/1970 structure -> DROPPED (upside < 7).
- (2026-11-07) Nash late gravity theory ("An Interesting Equation", 2003-2015; sites.stat.psu.edu/~babu/nash/intereq.pdf).
  Nash tensor = field equation of S = int sqrt(-g)(2 R_mn R^mn - R^2) (pure quadratic / Stelle-type gravity; my
  hand derivation agrees with the literature's action). Already picked up: Aadne-Gron 2017, Lake 2017 (arXiv
  1703.02653), Channuie-Momeni-Al Ajmi (matter added, arXiv 1808.06483), Chakrabarti et al. (arXiv 2208.02561),
  "Generalized Nash" + Einstein-Hilbert term (arXiv 2607.22126, Jul 2026). "Matter problem" is not open in the
  formal sense (action -> standard coupling); real issues = known Stelle-family ghosts + no Newtonian limit.
  Not missed, not big -> DROPPED. Nash personal papers: no public handwritten archive found (Princeton finding
  aids: direct requests redirect to /challenge = bot check; handwritten items OFFERED at Christie's Oct 2019,
  buyers unknown). His Princeton web folder IS public: web.math.princeton.edu/jfnj/texts_and_graphics/ (typed
  files 2007-2014: agencies/cooperative games, ideal money, gravity, India 2007, a 2014 class). Gravity folder has
  possibility.txt (23 Feb 2007): Nash's own idea for matter = Einstein-style fusion of EM field + metric into a
  nonsymmetric 16-component g_ij, rederive his R_ij/R Lagrangian -> mass from EM fields. Not checked whether the
  Nash-gravity papers discuss it. My judgment: upside < 7 (EM-mass idea conflicts with proton mass from the
  strong force; nonsymmetric unified theories = Einstein 1945-55, Moffat NGT). Do not download sav10.tar.gz (rule 8).
- L-001 Riemann 27 Bl. 14v: Machin-type pi/arctan formulas. Correct but closed field
  (Stormer 1899). Historical curiosity only. DROPPED. (details kept below for reference)
- L-002 Riemann 3, printed Goettinger Nachrichten 9.12.1863 p.384 (Bl. 15v): the
  mathematical class's prize question for Nov 1864 = TWIN PRIME CONJECTURE ("ob die
  Anzahl der Primzahlen, die nur um zwei Einheiten verschieden sind, unendlich ist,
  oder nicht"). Not in standard histories found (Britannica, arXiv 1405.5996 credit
  de Polignac/Staeckel/Hilbert/Landau/Brun). No Riemann approach found: Bl. 3r
  calculations = Riemann-Siegel material (mined by Siegel 1932, who reported no such
  approach). Historical only -> DROPPED.
- Riemann 3 Bl. 21r letter drafts (1859): says Dirichlet "tried a similar path four
  years ago" and hit difficulties. History -> DROPPED.
- Riemann 27 Bl. 16v (Dirichlet principle), 39r (classical axisymmetric reduction),
  19r (research-programme quote, printed in Werke) -> DROPPED.

### L-001 · DROPPED (not big) · Riemann computing Machin-type pi formulas
- **Where:** Riemann, Cod. Ms. B. Riemann 27 (1850-55), Bl. 14v. Scan:
  https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3206767:00000027/full/1600,/0/default.jpg
  (canvas 26; verify label 14v in targets/riemann/pages/b27/thumbs/inkmap.tsv)
- **Verbatim (formulas):** "(1) = (1/2) + (1/3) = 2(1/3) + (1/7) = 2(1/5) + (1/7) + 2(1/8)
  = 3(1/7) + 2(1/8) + 2(1/18) = 5(1/7) + 2(1/18) - 2(1/57)"; "(1/70) = (1/99) + (1/239)";
  "(239)^2+1 = 338.169 = 2.13^4"; "57^2+1 = 13.250"; "(1/307) = (1/597) + (1/632)"; ~30 such.
  Interleaved with a letter draft beginning "Meine liebe Marie!" (his sister).
- **Plain English:** "(1/n)" = arctan(1/n). Riemann is building formulas for pi/4 as sums of
  arctangents, by factoring n^2+1 (the Gauss / later Stormer 1896-99 method). Also a table of
  powers of 2 mod 37 and square roots of -1 mod primes (same method).
- **Verified:** 30/30 arctan relations and 13/13 factorizations exact (integer Gaussian-integer
  check): targets/riemann/verify/b27_14v_arctan.py. Two unclear lines excluded.
- **Why it might matter (interpretation):** historical: Riemann's interest in pi formulas is not
  mentioned anywhere I found. Scientific: none. Every identity is small and lies inside modern
  exhaustive tables; theory closed by Stormer (1899). Not the mission's target.
- **Novelty check:** web search "Riemann Nachlass arctangent Machin formula ..." -> no Riemann
  mentions; background sources credit Machin/Euler/Gauss/Simson (maths.tcd.ie/~nhb/pi.pdf);
  field still active (arXiv 2601.10300). Status OPEN (history), not verified new.
- **Next:** none for the mission. A historian could check Gauss's Nachlass for the source.

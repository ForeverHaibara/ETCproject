# ETC Source Data Errata

[中文](etc-source-errata.md) · [English](etc-source-errata.en.md) · [Repository guide](../README.md#en)

This inventory draws on local ETC snapshots, import patches, reviewed recipes, tests, and review notes. Each ID denotes `X(n)`, and `{i,j}` denotes the line through `X(i)` and `X(j)`. The live pages may have changed. A `seed` is a recipe maintained for an individual center. `SKIP source-error` explicitly excludes an entry.

## HTML, entry boundaries, and duplicate entries

The importer applies these repairs on read and preserves the raw HTML. It matches the Part and the actual content and logs the SHA-256 digest. See the [source patches](../tools/triangle_center_sources.py#L6) and [boundary and patch tests](../tools/test_source_errors.py#L582).

| Part | Entry | Source issue | Catalogue handling |
| --- | --- | --- | --- |
| 1, 31, 35 | 164, 60349, 68618 | The heading is missing the closing parenthesis in `X(n`. | Close the parenthesis. |
| 6 | 10043 | `p&gt;` joins the incidence list to the preceding `where p=…, q=…` clause. | Restore the paragraph break so the importer can extract coordinates and line intersections. |
| 28 | 54357 | The HTML anchor `id="X54357)"` has an extra `)`. | Fix the anchor so the preceding entry ends at the correct boundary. |
| 28 | 54980 | Two entries share an ID and match after whitespace removal. | Keep the last copy. If the copies differ, halt the import for review. |
| 29 | 57621 | The anchor is `X57621`, while the heading says `X(57622)`. | Change the heading to `X(57621)`. |
| 34 | 66288 | Two distinct complete definitions share an ID. | Quarantine both and mark the ID `SKIP source-error`. The intended IDs are unresolved. |
| 34 | 67713 | The HTML anchor `id="X67713 "` has a trailing space. | Trim the space to restore the entry boundary. |
| 36 | 71412 | The anchor is `X71412`, while the heading says `X(714112)`. | Change the heading to `X(71412)`. |

## Coordinates, coefficients, and family formulas

See the [source review](triangle-centers-source-review.md#L44), [regression tests](../tools/test_source_errors.py), and [reviewed seeds](../data/seeds.txt). The PB results come from the [family audit](triangle-centers-uncovered.md#L477) and the local cache file `reports/reviews/pb-printed-36-audit.json`.

| Entry | Source issue or observed discrepancy | Catalogue handling and evidence |
| --- | --- | --- |
| 5500 | The Shinagawa coefficients mix terms of different dimensions. The cyclic barycentric marker also has only one colon. | Seed the printed cyclic polynomial. It lies on the Euler line in both samples. |
| 5507 | The printed coordinates disagree with the stated radical center and line `{600,4640}`. | Construct the three circles independently and seed their radical center. |
| 5601, 5602 | The printed coordinate signs for the two Auriga branches are swapped. | Distinguish the branches by the convention that the first Auriga triangle's A-vertex lies on the same side of BC as A. Use the verified perspectors. |
| 7985 | A soft hyphen appears where the formula needs a minus sign. | Seed the expression with a minus sign. The resulting point agrees with `{726,3241}`. |
| 10685 | The last two degree-12 terms are missing a `+` between them. | An independent construction using the two Brocard points and their anticevian triangles confirms `+`. A minus sign also restores homogeneity but gives a different point. |
| 11619 | The printed trilinears give a different point from the circle center named in the heading and miss `{2492,2780}`. | Take the circumcenter of X(5), X(6), and X(22). Independently intersecting the perpendicular bisectors gives a point on the stated line. |
| PB preamble for 11753–11788 | In starred groups, changing the sign of `S` only outside the radical breaks the preamble's diameter-circle condition. | Recompute the sign of `S` inside `U` for each group. Verify all 36 perspectors independently from vertex matrices. |
| PB 11762, 11763, 11765, 11768, 11769, 11770, 11771, 11772, 11774, 11775, 11776, 11777, 11778, 11779, 11784, 11785 | Sixteen printed formulas still disagree with the independent perspectors after expanding `U` for the correct group. The printed transformations for 11770 and 11779 are mixed up. | Keep the verified family positions and add seeds for 11761, 11770, 11779, and 11788. The focused comparison found that the printed coordinates for 11761 agree. |
| PB 11755, 11764, 11773, 11782 | The printed coordinates have unbalanced parentheses. The incidence list for 11755 also starts with a stray backslash. | For 11755, intersect two verified lines. The result agrees with the coordinates after balancing parentheses and expanding `U`. Keep the other recipes verified by the independent family audit. |
| PB 11788 | A missing multiplication makes the printed expression nonhomogeneous. | Use the independently constructed perspector. |
| 12025 | The printed formula is nonhomogeneous. The geometric review of the original post identifies the result as the Feuerbach point X(11). | Mark `SKIP source-error`. Both terms give points on the same line, so collinearity alone cannot identify a corrected expression. |
| 15276 | The coefficient `fd12` should be `12`. | Correct the seed following the user's geometric verification. |
| 32584 | The printed formula mixes degree-9 and degree-10 terms and disagrees with the center of the mutual polar conic. | Mark `SKIP source-error`. An independent polar-line matrix gives X(115) as the center. |
| 38493, 38494, 38538, 38546, 38547, 38549, 38550 | Some `bc` terms are printed as `abc`. The expression for 38494 also has a valid `abc(b+c-2a)` term. | Seed 38493 and 38494 from independently checked vertex constructions. Use the verified VU two-circle rule for the other five. |
| Second VU preamble and 38923–38929 | An extra `a` in `8a a^4` makes the expression nonhomogeneous. | Derive the formula independently from the circumcevian construction and confirm `8a^4` by symbolic comparison. |

## Incorrect relations, incidences, and references

The evidence includes independent constructions, user verification, and comparisons with coordinates and incidence lists. Agreement on a few sample triangles supports the catalogue choice. See the [source review](triangle-centers-source-review.md#L137), [manual review and upstream repairs](triangle-centers-consensus-review.md#L53), and [reviewed seeds](../data/seeds.txt#L250).

| Entry | Source issue | Catalogue handling and evidence |
| --- | --- | --- |
| 4201, 13740 | Each entry claims to be the complement of the other. | The explicit intersection for 4201 agrees with the printed coordinates. Use that intersection and keep 13740 as its complement. |
| 7581, 7582 | The stated point reflections in X(7601) and X(7602), respectively, disagree with the coordinates, Euler line, and several incidences. | Use intersections that agree with the coordinates. |
| 7742 | The stated circumcircle inversion of X(5560) gives a different point. | Use the user-verified intersection of `{1,3}` and `{22,1612}`. |
| 9834, 9835 | Some printed relations for 9835 mix up the Auriga orthocenter branches. | Construct the two orthocenters independently. They are reflections of each other in X(55). |
| 9858 | The complement-of-X(20012) claim conflicts with the explicit weighted definition, coordinates, and native incidences. | Use an intersection consistent with the weighted definition. |
| 13137 | The entry identifies `{115,523}` as the Simson line of X(98). | Reflect across the line through the actual pedal points. This agrees with the printed coordinates and four native incidences. |
| 14087, 14088, 14090 | The anticomplement of X(14084), a subsequent conjugation, and an intersection involving X(14083) conflict with BSS, the printed coordinates, and compatible conjugate definitions. | Keep the compatible coordinates and conjugations. The user independently verified the singular foci 14083 and 14084. Fixing the upstream recipes also resolves 60545. |
| 14624 | The heading's intersection `{1,10469}` ∩ `{6,8}` disagrees with the printed coordinates. | Select `{2,1240}` ∩ `{10,1400}`, which restores downstream 37868. The exact heading line or endpoint at fault remains undetermined. |
| 14821 | The line `{11709,14933}` disagrees with the GL construction, printed coordinates, and barycentric product. | Keep the product seed. The 6–9–13 triangle gives near-collinearity, but the exact determinant is nonzero. |
| 14838 | The complement input in the heading is `1557` and should be `1577`. | Use `C 1577`, which agrees with the body and incidence list. Downstream 40473 and 40497 recover. |
| 18131, 34419 | The heading references should read `14597 → 15497` and `46 → 48`, respectively. | Seed the intersections based on the user's review of the Hyacinthos posts and geometry. |
| 20211, 22654 | 20211 claims to be the anticomplement of 22654, while 22654 claims to be the complement of 20211. Both claims conflict with the verified positions. | Fix both entries at compatible intersections. Downstream 34863 recovers. |
| 34307, 34575 | The line `{14452,15767}` for 34307 is incorrect. Two properties involving 8937 are incorrect for 34575. | Keep the coordinates based on the user's verification against Q004 and Euclid 19. |
| Vietnamese anticevian preamble | The index assigns `(2,4)` to 39192 and `(2,5)` to 29192, and lists `(3,5)` twice. | Read the inputs from the headings. 39191/39192 correspond to `(2,4)`/`(2,5)` and 39194/39195 to `(3,4)`/`(3,5)`. |
| 39204, 39205 | The headings describe minor-axis vertices, but `{2,1341}` is the major axis. | Project onto the ellipse's minor axis. The line `{2,1340}` in 39208 and 39209 agrees with that axis. |
| 40822, 72796 | The intersection endpoints in the headings should read `6 → 2` and `8 → 80`, respectively. | Use compatible intersections confirmed by the user. Fixing 40822 also restores 40807. |
| 48720 | The stated `cevapoint(115,1043)` disagrees with the Dao / X-parabola-tangential perspector. | Use the printed coordinates following independent user verification. |
| 71989, 72498, 72939, 72941, 73051 | The heading endpoints should read `27196 → 27186`, `36063 → 36036`, `1 → 3`, `1 → 3`, and `11154 → 1154`, respectively. | The corrected intersections agree with the printed coordinates and comparable incidences. 72939 and 73051 each list two lines. Fixing 71989 restores the existing reflection recipe for 72215. |

## Formatting, formula syntax, and misplaced fields

See the [source review](triangle-centers-source-review.md#L65), [coordinate review](triangle-centers-source-review.md#L258), and [seeds from that review](../data/seeds.txt#L344).

| Entry | Source issue | Catalogue handling |
| --- | --- | --- |
| 5945, 5959, 6160 | A stray backslash before `Barycentrics`, `tthese lines`, and `Trlinears`, respectively. | Use reviewed coordinates, an ideal-point marker, and converted trilinears, respectively. |
| 10228, 11811, 51777 | The label and formula are in separate blocks, or the cyclic marker `: :` is missing. | Seed the first printed cyclic component for each point. |
| 23032–23034 | The source defines `x=sec(…)` and leaves the reader to infer the cyclic definitions of `y,z`. | Write the cyclic quantities explicitly in the seeds. |
| 26653, 26842 | An incidence list appears in the `Barycentrics` field. | Use verified line intersections. The two previously disputed incidences for 26842 agree after fixing 1071. The field placement is a separate issue. |
| 36721, 36731 | An unrelated parameter precedes the coordinates, separated by a semicolon. The body refers to the entries as 38721 and 38731. | Remove the prefix and verify coordinates and incidences under the correct IDs. |
| 38439 | The denominator has an extra closing parenthesis. | Remove the extra parenthesis in the seed. |
| 39203, 39301, 39303 | `SSqrt` is misspelled. Some self-references for 39301 and 39303 read 30301 and 30303. | Use verified ellipse-axis and center-of-curvature constructions. |
| 40139 | The first barycentric component `a*(a + sqrt(t + a^2)` is missing the outer closing parenthesis. | The entry also has trilinears for reference. Solving for the implicit positive parameter remains deferred. |
| 41156 | The phrase `lies the Terzic circle and these lines` is missing `on`. | Accept this heading pattern and continue to validate the target ID. |
| 46183, 53806, 62503 | The incidence lists refer to their own entries as 46193, 537, and 6249, respectively. | Seed the ideal directions after individual review. |
| 54028, 54029, 70832, 70855 | The first two entries omit the closing parenthesis in the incidence-list ID. The last two use `X{n)`. | Accept these specific malformed delimiters and continue to validate the target ID. |
| 72483 | The second closed form has an extra opening parenthesis. The `u/v/w` portion of the first form is also malformed. | Balance the second form and expand the symmetric quantities. Compare against an independent numerical root for equal-length cevian segments. |
| 72513 | The printed cyclic coordinates lack a `Barycentrics` label. | Seed the printed expression. For related center 72514, an equivalent reduced expression improves numerical stability. |
| 72698–72701 | The three coordinates are comma-separated and followed by `: :`. | Seed the verified first cyclic component for two roots and obtain the other two points by reflection. |

## Source conflicts with unresolved causes

| Entry | Current evidence and limits |
| --- | --- |
| 7065, 8064, 32072, 39038 | An independent extra-triangle perspector, isogonal conjugate, Lucas inner triangle centroid, and center of a five-point hyperbola, respectively, support the catalogue positions. Some incidences still disagree. The disputed lines for 7065, 32072, and 39038 are `{219,6862}`, `{356,8496}`, and `{2549,24185}`. Their endpoints still need independent checks. |
| 14079 | Keep the position consistent with the barycentric product. Two of the four listed lines conflict. The user independently verified the singular-focus definitions of 14083 and 14084. The disputed incidences remain open. |
| 3136, 3995, 4359 | The Euler-line definition for 3136 conflicts with its complement claim, and its printed coordinates could not be parsed directly. The mutual complement claims for 3995 and 4359 conflict. Historical sample comparisons help locate the discrepancies. |
| 8430, 38513, and other cases from the consensus review | The catalogue uses positions supported by the coordinates and a majority of properties. The weighted support was 13/14 for 8430 and 24/26 for 38513. The correctness of individual headings or geometric definitions remains unresolved. |
| 27 Gemini headings | New template candidates for 25395–25400, 25953, 26181–26199, and 28820 differ from the previous positions in the sample comparison. The catalogue keeps the compatible existing candidates. Possible causes include the heading, Gemini table, coordinates, or upstream inputs. |

A historical full-source scan found 184 structural hints involving headings and incidence lists. The published diagnostic retained 168 over a different scope. These are leads for review. See the [review history](triangle-centers-source-review.md#L193), [consensus review](triangle-centers-consensus-review.md), and [Gemini comparison](triangle-centers-source-review.md#L375).

## Resolved false alarms and implementation limits

| Entry | Established cause |
| --- | --- |
| 31608, 38941, 72780, 40619 | The old parser dropped a reference-triangle qualifier, the second endpoint of a reflection line, or the tail of a compound relation. The resulting recipes expressed different relations from those on the page. |
| 1071, 10202, 26842 | An older GeoGebra implementation returned the wrong position for native center 1071. Repairing it restored agreement for the midpoint relation of 10202 and both disputed incidences of 26842. The other native overrides are also tracked as runtime issues. |
| 8037, 72514 | A removable `0:0:0` base point affected 8037 in the obtuse sample. Double-precision cancellation affected the high-degree polynomial for 72514. High-precision evaluation supports the printed coordinates and incidences for 72514. |
| 32472, 64802 | The cyclic coordinates sum to zero, so these are ideal points. Finite candidates from the earlier voting or construction code do not establish an error in the source coordinates. |
| 39160, 39161, 39164, 39165, 39641, 39642, 51539, 51540, 65627, 65628 | These centers are nonreal in general position. Centers 5000–5003, 11065, and 11066 are nonreal only for some triangles. |
| 13580, 13581 and 368, 370, 1144, 5373, 5394, 5626, 40139 | The first two entries lack an explicit local definition of `J`. The catalogue uses independent conjugate relations. The remaining entries require implicit solving or root selection. These limitations leave the geometric definitions open. |

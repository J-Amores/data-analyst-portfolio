# Data Analyst Portfolio

**John Amores** · Software engineer working in cloud platforms, data analytics and enterprise
telecom systems.

Case studies in applied data analysis. Each one starts from a decision somebody actually has to
make, answers it against real data, and is written so a reader can find the point where it might
be wrong. Every study ships three things: a **README** that summarises it, an **interactive report**
served as a GitHub Page, and the **executed notebook** behind both.

---

## Case studies

### [CS05 · One-hit or repeat: what separates a small channel that trends twice?](CS05-Youtube-Statistic-Study/)

205 days of the US YouTube trending board, cut down to the channels an independent creator actually
competes with. The creator believed trending was luck, so the study was built to be losable: if it
were luck, channels that went on to trend again would have looked no different beforehand.

They did look different. Channels that trended more than once were already ahead on their very
first trending video, before any repeating had happened — 4.84% engagement against 3.05%, measured
on 445 channels against 899. But none of the five settings a creator owns turns out to be the lever
that gets you there, and the study says so rather than manufacturing a to-do list. The useful
result is a subtraction: the packaging work to stop doing.

[**Read the report →**](https://j-amores.github.io/data-analyst-portfolio/CS05-Youtube-Statistic-Study/) · [**Notebook →**](CS05-Youtube-Statistic-Study/analysis.ipynb) *(78 cells, executed)* · [**Summary →**](CS05-Youtube-Statistic-Study/)

`Kaggle datasnaek/youtube-new, US slice` · 40,949 rows · 2017-11-14 → 2018-06-14

---

Four more studies are finished offline and land here as they're prepared for publication: UK online
retail RFM segmentation, a bank marketing campaign, Amazon product reviews, and a Google Analytics
study.

## How these are built

The analysis standards matter more than the topic, so they are stated up front rather than buried:

- **Medians of per-video rates, never pooled sums**, wherever a long tail would otherwise do the
  talking. In CS05 the top 1% of videos hold 19.45% of all views.
- **Clustered bootstrap intervals** wherever one entity can contribute more than one row. A naive
  row-level interval on the CS05 data is roughly three times too narrow.
- **Detection rules declared before computing**, with multiple-comparison correction reported
  alongside and never used to promote a finding into significance.
- **Coverage stated as a number.** When a question can only be answered for part of the data, the
  part it could not reach gets a sentence and a count, not silence.
- **Effect sizes in the units the reader counts** — reactions per upload, money, people — with the
  estimate's range attached and the parts of that range that are *not* included named explicitly.
- **A conclusion that answers analytically.** Where the honest answer is "no lever here," that is
  the finding.

Built with Python, pandas, numpy, scipy and matplotlib. Charts and their interactive twins render
from one shared spec, so a static PNG and the report it appears in cannot drift apart.

Raw source tables are linked, not redistributed. Every report and notebook ships with its outputs
baked in, so nothing here needs a download to read.

## Contact

- **LinkedIn** — [linkedin.com/in/john-amores](https://linkedin.com/in/john-amores)
- **Email** — johncamores@gmail.com

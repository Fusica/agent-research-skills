# Venue Quality Policy for UAV/CV/Robotics/RL Research

This policy is a user-defined search and review filter. Its purpose is to keep literature search focused on reputable venues for UAV, computer vision, robotics, and reinforcement learning work. It is not a legal or universal classification of publishers.

## Core Rule

Exclude all MDPI venues and all records matching the hard blacklist before using papers for deep research, literature search, literature review, novelty assessment, or related work writing.

When quality matters more than recall, use strict target-venue filtering:

```bash
python ${CODEX_HOME:-$HOME/.codex}/skills/deep-research/scripts/filter_publications.py \
  --input merged.jsonl \
  --output filtered.jsonl \
  --report quality_filter_report.json \
  --strict-target-venues \
  --allow-preprints
```

`--strict-target-venues` keeps only papers from the target venue lists below plus arXiv/preprints when `--allow-preprints` is set.

## Target Venues

### Tier 1: Core Targets

Robotics and UAV systems:
- Science Robotics
- The International Journal of Robotics Research / IJRR
- IEEE Transactions on Robotics / T-RO
- IEEE Transactions on Automation Science and Engineering / T-ASE
- IEEE Robotics and Automation Letters / RA-L
- Robotics: Science and Systems / RSS
- IEEE International Conference on Robotics and Automation / ICRA
- IEEE/RSJ International Conference on Intelligent Robots and Systems / IROS
- Conference on Robot Learning / CoRL

Computer vision and multimedia:
- IEEE/CVF CVPR
- ICCV
- ECCV
- IEEE Transactions on Pattern Analysis and Machine Intelligence / TPAMI
- International Journal of Computer Vision / IJCV
- IEEE Transactions on Image Processing / TIP
- IEEE Transactions on Multimedia / TMM
- IEEE Transactions on Circuits and Systems for Video Technology / TCSVT

AI/RL:
- NeurIPS
- ICML
- ICLR
- AAAI
- IJCAI
- AAMAS
- JMLR

### Tier 2: Strong Related Venues

- Journal of Field Robotics
- Autonomous Robots
- Robotics and Autonomous Systems
- IEEE Robotics & Automation Magazine
- Engineering Applications of Artificial Intelligence / EAAI
- Pattern Recognition
- Computer Vision and Image Understanding / CVIU
- WACV
- BMVC
- ACCV
- IEEE CASE
- IEEE Transactions on Neural Networks and Learning Systems / TNNLS
- Neural Networks

### Tier 3: Conditional Venues

Use only when the task clearly matches the venue:
- IEEE Transactions on Intelligent Transportation Systems / T-ITS
- IEEE Transactions on Geoscience and Remote Sensing / TGRS
- ISPRS Journal of Photogrammetry and Remote Sensing
- Remote Sensing of Environment
- Automatica
- IEEE Transactions on Automatic Control / TAC
- Control Engineering Practice

## Hard Publisher and Journal Blacklist

Hard-block by any of these signals:
- Publisher contains a blocked publisher name.
- DOI starts with a blocked DOI prefix.
- URL/PDF domain contains a blocked domain.
- Venue/journal title exactly matches a blocked journal title.

### Publisher Blocks

Always exclude records from:
- MDPI
- Frontiers Media
- Hindawi
- OMICS International
- WASET
- Scientific Research Publishing / SCIRP
- Science Publishing Group
- Academic Journals
- IOSR Journals
- IISTE
- David Publishing
- MedCrave
- Herald Scholarly Open Access
- Crimson Publishers
- Juniper Publishers
- Longdom Publishing
- Austin Publishing Group
- Bentham Open
- Allied Academies
- Baishideng Publishing Group
- Gavin Publishers
- Remedy Publications
- Jacobs Publishers
- Pulsus Group
- SciRes Literature
- Open Access Text

### DOI Prefix Blocks

- `10.3390` — MDPI
- `10.3389` — Frontiers
- `10.1155` — Hindawi

### Domain Blocks

- `mdpi.com`
- `mdpi-res.com`
- `frontiersin.org`
- `hindawi.com`
- `omicsonline.org`
- `waset.org`
- `scirp.org`
- `sciencepublishinggroup.com`
- `academicjournals.org`
- `iosrjournals.org`
- `iiste.org`
- `davidpublisher.com`
- `medcraveonline.com`
- `heraldopenaccess.us`
- `crimsonpublishers.com`
- `juniperpublishers.com`
- `longdom.org`
- `austinpublishinggroup.com`
- `benthamscience.com/open`
- `alliedacademies.org`
- `baishideng.com`
- `gavinpublishers.com`
- `remedypublications.com`
- `jacobspublishers.com`
- `pulsus.com`
- `sciresliterature.org`
- `oatext.com`

### Journal Title Blocks

Always exclude exact journal-title matches:
- Drones
- Sensors
- Remote Sensing
- Applied Sciences
- Electronics
- Machines
- Robotics
- Aerospace
- AI
- Algorithms
- Information
- Mathematics
- Entropy
- Vehicles
- Journal of Imaging
- Big Data and Cognitive Computing
- Scientific Reports
- IEEE Access
- Heliyon
- PLOS ONE
- PeerJ Computer Science

Do not block legitimate titles that merely contain a similar substring, such as `Remote Sensing of Environment`.

## Search Behavior

- Deep research Phase 1/2 must filter raw search results before writing `paper_db.jsonl`.
- Literature search must run the filter before presenting ranked results.
- Literature review must synthesize from filtered paper databases only.
- Keep arXiv/preprints only as supplementary evidence and mark them as preprints.
- If a blocked record looks genuinely important, mention it separately as "excluded by user quality policy" rather than using it as evidence.

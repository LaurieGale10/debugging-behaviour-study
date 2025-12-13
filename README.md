# Repository Overview
This repository contains the study materials and analysis for the *An Investigation Into K-12 Students' Debugging Behaviour in Python* paper.

As we do not have permission to publish students' data, none of this code will properly run. We still make it publicly available to document the analysis we performed - just view `log_data_analysis.pdf` or `log_data_analysis.html`.

The repository has the following structure:
- `log_data_analysis.pdf/html/ipynb`: A jupyter notebook containing the analysis reported in the paper (we did not have ethical approval to publish students' log data so the running the notebook will result in errors).
- `analysis`: Materials used to analysis the log data, including:
  - `codebook.pdf`: The codebook used to code the log data (also in programmatic form in `codebook.json`).
  - `loading_services/`: Directory of files used to analyse the log data.
  - The utility files used for data analysis, such as retrieving students and exercise attempts with a particular code (`core_filter_functions.py` and `filter_functions.py`), statistical analysis (`stats_functions.py` and `stats_helper_function.py`), and data visualisation (`visualisation.py`).
- `results`: The final codebook with frequencies per student and exercise attempts (`codebook_frequency.csv`).
- `study_materials`
  - `debugging_exercises`: The debugging exercises that students attempted. Contains the original erroneous Python programs posed to students (`*_original.py`) and the corrected versions (`*_correct.py`).
  - `student_survey.pdf`: The survey students completed at the end of the study.
- `website`: Directory containing the code needed to run the website students used to complete the study. See the `README.md` in this directory for more detailed setup instructions.

## License
This repository is licensed under the terms of the MIT license (see `LICENSE.md`).

## Further Details
- Authors
  - Laurie Gale (ORCID: [0009-0004-4299-6704](https://orcid.org/0009-0004-4299-6704))
  - Sue Sentance (ORCID: [0000-0002-0259-7408](https://orcid.org/0000-0002-0259-7408))
- Period of data collection: 2023-01 - 2023-02.

### Log Data Format
```
{
    (optional) "error": {
        "error: string //The error message thrown by the program, only present in a log if "compiled" is false
    },
    "compiled": boolean, //Whether the program successfully ran or not. Will be false if the program contains syntax or runtime errors
    "snapshot": string, //The program at the time of running, expressed as a string
    "timestamp": int //The time the program was ran at
}
```
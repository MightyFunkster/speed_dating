# Beauty and the Beholder: Exploring the Impact of Attractiveness Perception on Second Date Success

## What This Project Does
This project is a Python analysis of this speed dating dataset: https://data.world/annavmontoya/speed-dating-experiment. An explanation of all the column meanings and the background of the experiment can be found in the speed dating data key document.

- This data comes from a speed dating experiment in which many different people participated in dates.
- The study concerned five main attributes: **attractiveness, sincerity, intelligence, fun and ambition**.
- Each row in the table concerned a particular date. The columns **iid** represented a particular individual. The column **pid** represents the iid of the other individual on the date (e.g. iid's partner).
- Each participant would rate themselves on these five attributes (scale 1 - 10, represented by columns attr3_1, sinc3_1, intel3_1, fun3_1 and amb3_1) before dating begins. (For a particular row/date these are the self-ratings as stated by **iid**).
- Each participant allocates 100 points across these five attributes in what they look for in a date i.e. which attributes are most important. These are represnted by pf_o_att, pf_o_sin, pf_o_int, pf_o_fun and pf_o_amb. (For a particular row/date these are the preferences as stated by individual **pid**, **not iid**).
- After each date, each participant would rate their partner on a scale of 1 - 10 for these five attributes (represented by columns attr_o, sinc_o, intel_o, fun_o and amb_o).
- Each row contains the gender of the person (**iid**) where 1 is male and 0 is female.
- For each row, we have many values but for this study the most relevant were the columns representing the five attributes that an individual rated themselves on, the values that their date (**pid**) rated an individual (**iid**) on a particular date across these five attributes and the initial preference allocation.
- We have a **dec_o** column representing the decision of the partner (**pid**). If the value is 1, they agreed for a second date. If the value is 0 they did not.

This study explores:
- The average allocation of preference initially by gender (pf_o_att, pf_o_sinc etc.).
- The actual most important preference/feature through a random forest analysis of ratings received (attr_o, sinc_o etc.) and second date success (dec_o).
- The influence of average attractiveness rating received (attr_o) on second date success (dec_o).
- How each level (2, 3, 4, ..., 10) of self rating of attractiveness effects second date success i.e. does an individual's confidence in their attractiveness alone increase second date potential.
- The impact of self-perceived attractiveness (comparing the difference between an indivdual's self rating of attractiveness with their average attractiveness rating received on their dates and how this drives second date potential).

## How To Use This Project

- First read the [Speed Dating Data Key.doc](https://github.com/MightyFunkster/speed_dating/blob/main/Speed%20Dating%20Data%20Key.doc) provided by those in charge of the experiment. This gives an entire overview of the experiment as well as an explanation of all the initial columns provided.
- Give the [speed_dating.csv](https://github.com/MightyFunkster/speed_dating/blob/main/speed_dating.csv) a quick skim through, specifically keeping in mind the explanation given under 'What This Project Does'. This allows you to see how the rows are arranged, the fact that one row represents one perspective of a particular date, the fact we have two rows per date and will also allow you to see which individual (iid or pid) a particular set of attributes belong to on a particular date in the original dataset.
- Read the database schema to understand the data I am using, why and how these tables link together and how the data has been transformed from the original dataset.
- Only after this should you start executing code. Whilst I do provide explanations and justifications for different sections of code on the Jupyter Notebook, they are brief and will make much more sense once you understand the column meanings, how the data fits together and what the data represents.
- The first non-analysis cells should be ran in order (.csv importing, data pre processing and database creation) as you shouldn't be creating a database until it has been cleaned.
- Each analysis section can be run in any order (e.g. you can run the code representing the impact of self-perceived attractiveness before the analysis of initial preference allocation) but within each section cells should be ran in order (function definitions are provided in these cells and need to be run before these functions can be called).

## To-Do

- Upload updated database documentation.
- Link files to the readme
- Finish transferring code from .py to Jupyter Notebook.
- Improve old functions, particulalry confidence_boxes.py since it is incredibly slow. Considering using more/better SQL commands instead of running most of it through Pandas.
- Cross-validation for number of nearest neighbour values.
- Test results without using data imputation and include in Jupyter Notebook.
- Test results with larger values of NULL values required for row deletion and include in Jupyter Notebook.
- Include data pre processing function to delete rows that have missing values for dec_o along with justification.
- Improve functions by introducing more helper functions for repeated code.
- Include Notebook section explaining variance in attractiveness ratings.
- Include installation section on readme explaining libraries and Jupyter Notebook.
  
## How to Contribute

This is my first Github repository so please suggest any changes to code or database layout.

### Reporting Issues

If you find a bug, have a question, or want to suggest an improvement please [open an issue](https://github.com/mightyfunkster/speed_dating/issues).

### Making Changes

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and commit them with clear messages.
4. Push your changes to your fork.
5. [Open a pull request](https://github.com/mightyfunkster/speed_dating/compare) with a detailed description of your changes.

### Feedback

Please provide feedback on the project layout, documentation or any other aspect. It would be greatly appreciated.

## Changelog

### [Version 1.0.0] - 05/12/2023

#### Added
- [data_preprocessing.py](https://github.com/MightyFunkster/speed_dating/blob/main/data_preprocessing.py) containing all the pre processing code (deleting NULL values, deleting missing pairs and imputating data).
- [create_tables.py](https://github.com/MightyFunkster/speed_dating/blob/main/create_tables.py) containing code to create the database schema.
- [attribute_importance.py](https://github.com/MightyFunkster/speed_dating/blob/main/attribute_importance.py) containing code to perform a random forest model for feature importance on the attribute that most drives second date potential.
- [confidence_box.py](https://github.com/MightyFunkster/speed_dating/blob/main/confidence_box.py) containing **very** slow code to create a line and box plot showing how confidence in your own attraction affects second date potential.
- [self_perception_attraction.py](https://github.com/MightyFunkster/speed_dating/blob/main/self_perception_attraction.py) containing code to analyse what role accurate self-perception of attraction plays on second date success.

#### Changed

#### Removed/Archived

### [Version 2.0.0] - 07/12/2023

#### Added
- Added [Speed Dating Data Key.doc](https://github.com/MightyFunkster/speed_dating/blob/main/Speed%20Dating%20Data%20Key.doc) to main folder.
- Added links to the [Speed Dating Data Key.doc](https://github.com/MightyFunkster/speed_dating/blob/main/Speed%20Dating%20Data%20Key.doc) and [speed_dating.csv](https://github.com/MightyFunkster/speed_dating/blob/main/speed_dating.csv) to the 'How to use this project section'.
- Added a [Deprecated Folder](https://github.com/MightyFunkster/speed_dating/tree/main/Deprecated) to store old .py files.
- Added the updated [speed_dating_analysis.ipynb](https://github.com/MightyFunkster/speed_dating/blob/main/speed_dating_analysis.ipynb) which contains the new code.
- Added the [old presentation](https://github.com/MightyFunkster/speed_dating/blob/main/Deprecated/Beauty%20and%20the%20Beholder.pptx) to the [Deprecated Folder](https://github.com/MightyFunkster/speed_dating/tree/main/Deprecated).
- Added the [old database schema](https://github.com/MightyFunkster/speed_dating/blob/main/Deprecated/Database%20Documentation.pdf) to the [Deprecated Folder](https://github.com/MightyFunkster/speed_dating/tree/main/Deprecated).
- Moved the .csv to .db creation and the data pre processing to [speed_dating_analysis.ipynb](https://github.com/MightyFunkster/speed_dating/blob/main/speed_dating_analysis.ipynb).

#### Changed

#### Removed/Archived
- Moved old .py files ([data_preprocessing.py](https://github.com/MightyFunkster/speed_dating/blob/main/Deprecated/data_preprocessing.py), [create_tables.py](https://github.com/MightyFunkster/speed_dating/blob/main/Deprecated/create_tables.py), [attribute_importance.py](https://github.com/MightyFunkster/speed_dating/blob/main/Deprecated/attribute_importance.py), [confidence_box.py](https://github.com/MightyFunkster/speed_dating/blob/main/Deprecated/confidence_box.py) and [self_perception_attraction.py](https://github.com/MightyFunkster/speed_dating/blob/main/Deprecated/self_perception_attraction.py) to the [Deprecated Folder](https://github.com/MightyFunkster/speed_dating/tree/main/Deprecated).)

### [Version 2.0.1] - 08/12/2023

#### Added
- Added an overall analysis description cell at the beginning.
- Added table creation code.

#### Changed
- Updated .csv to .db description with explanation of included columns.
- Updated .csv to .db code to include pf_o columns.
- Updated the .csv to .db code with pf_o mappings to ensure names are consistent.
- Updated database creation to a function create_db that has as input the name of the csv file, the encoding type, the name of the db file and the csv columns to be included.
- Updated the delete_missing_values to take in pf_o columns as a parameter.
- Improved function descriptons.
- Created a list of base attributes outside of functions. Other column sets (_o, 3_1, pf_o) are now created from this base set.
- delete_null_values now takes in: columns_o, columns_3_1, columns_pf_o and null_no as input where the columns are the three sets of columns and null_no is the number of NULL values to use as threshold for row deletion.
- data_imputation now takes in columns_to_impute. This is the set of columns to perform data imputation on.
- Moved database connection inside table creation functions.
- Changed table creation function to one function per table.
- Included table creation for preferences table.

#### Removed/Archived


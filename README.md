# ALFlowLyzer

As part of the Understanding Cybersecurity Series (UCS), ALFlowLyzer is a Python open-source project to extract application layer features from network traffic for Anomaly Profiling (AP) which is the third component of the [**NetFlowLyzer**](https://github.com/ahlashkari/NetFlowLyzer).

ALFlowLyzer generates bidirectional flows from the Application Layer of network traffic, where the first packet determines the forward (source to destination) and backward (destination to source) directions, hence the statistical time-related features can be calculated separately in the forward and backward directions. Additional functionalities include selecting features from the list of existing features, adding new features, and controlling the duration of flow timeout. In the first version, it supports DNS protocol and in the next versions other protocols will be supported. For more information regarding the DNS flow definition, please refer to the corresponding paper in the [Copyright](#copyright-(c)-2024) section.

# Table of Contents

- [Installation](#installation)
- [Execution](#execution)
  * [Configuration File](#configuration-file)
  * [Argument Parser](#argument-parser)
- [Architecture](#architecture)
- [Extracted Features](#extracted-features)
  * [DNS Related](#dns-related)
  * [Statistical Information Calculation](#statistical-information-calculation)
- [Output](#output)
- [Copyright (c) 2024](#copyright-(c)-2024)
- [Contributing](#contributing)
- [Project Team members](#project-team-members)
- [Acknowledgement](#acknowledgement)


# Installation

Before installing or running the ALFlowLyzer package, it's essential to set up the necessary requirements on your system. Begin by ensuring you have both `Python` and `pip` installed and functioning properly (execute the `pip3 --version` command). Then, execute the following command:

```bash
pip3 install -r requirements.txt
```

You are prepared to install ALFlowLyzer. To proceed, execute the following command in the package's root directory (where the setup.py file is located), which will install the ALFlowLyzer package on your system:

### On Linux:
```bash
python3 setup.py install
```

### On Windows:
```bash
pip3 install .
```

After successfully installing the package, confirm the installation by running the following command:

```bash
alflowlyzer -h
```

```
usage: ALFlowLyzer [-h] [-c CONFIG_FILE] [-o] 
options:
 -h, --help            show this help message and exit
 -c CONFIG_FILE, --config-file CONFIG_FILE
                       JSON config file address.
 -o, --online-capturing
                       Capturing mode. The default mode is offline capturing. 
```


# Execution

The core aspect of running ALFlowLyzer involves preparing the configuration file. This file is designed to facilitate users in customizing the program's behavior with minimal complexity and cost, thus enhancing program scalability. Below, we outline how to prepare the configuration file and subsequently demonstrate how to execute ALFlowLyzer using it.

## Configuration File

The configuration file is formatted in `JSON`, comprising key-value pairs that enable customization of the package. While some keys are mandatory, others are optional. Below, each key is explained along with its corresponding value:

* **pcap_file_address** [Required]
  
  This key specifies the input PCAP file address. The format of the value should be a string.
  
  **Note**: At this version of ALFlowLyzer, we only support the `PCAP` format. For other formats such as `PCAPNG`, you must convert them to `PCAP`. To convert `PCAPNG` to `PCAP`, you can use Wireshark. If you prefer command-line tools, you can use the following command:

  ```bash
  tshark -F pcap -r {pcapng_file} -w {pcap_file}
  ```

  Replace `{pcapng_file}` with the path to your PCAPNG file and `{pcap_file}` with the desired output PCAP file name.

* **output_file_address** [Required]

  This key specifies the output CSV file address. The format of the value should be a string.

* **label** [Optional]

  This key specifies the value of the `label` column in the output CSV file address. The format of the value should be a string. The default value is `Unknown`.


* **number_of_threads** [Optional]

  This key specifies the number of threads to be used for all processes, including flow extraction, feature calculation, and output writing. The value must be an integer of at least `3`. The default value is `4`.

  It's important to consider that the optimal value for this option varies based on the system configuration and the format of the input PCAP file. For instance, if the PCAP file contains a large number of packets (e.g., more than 5 million) and they are all TCP packets, increasing the number of threads might be beneficial. However, if the packets represent a small number of flows and all related packets are contiguous, adding more threads could potentially slow down the program since there are fewer distinct flows.

  As a rule of thumb, the ideal value for this option typically falls between half the number of CPU cores (CPU count) and twice the CPU count. This helps balance computational resources without overwhelming the system. (`0.5 * cpu_count < best_option < 2 * cpu_count`)


* **feature_extractor_min_flows** [Optional]

  This key determines the minimum number of finished flows required for the feature extractor thread to initiate its work and extract features from these finished flows. The value must be an integer. The default value is `4000`.

  Selecting a high value for this option will consume more RAM since more flows will be stored in memory, potentially slowing down the entire program. Conversely, choosing a low value for this option can slow down the execution process, as it involves locking the finished flows list and then copying those flows for feature extraction. These two processes, locking and copying, are slow and can impede other program components.


* **writer_min_rows** [Optional]

  This key specifies the minimum number of ready flows (i.e., finished flows from which features have been extracted) required for the writer thread to begin its work of writing the flows to the CSV file. The value must be an integer. The default value is `6000`.

  Opting for a high value for this option will increase RAM usage since more flows will be stored in memory, potentially slowing down the overall program performance. Conversely, selecting a low value for this option can slow down the execution process, involving locking the finished flows list, copying those flows for the writing process, and performing I/O operations to write to the file. These three processes — locking, copying, and I/O — are slow and may impede other program components.
  
* **read_packets_count_value_log_info** [Optional]

  This key determines the minimum number of processed packets (i.e., the number of packets read from the PCAP file and assigned to a flow) required for the logger to log. The value must be an integer. The default value is `10,000`. This means that after processing every `10,000` packets, the program will print a statement indicating the number of packets analyzed.


* **check_flows_ending_min_flows** [Optional]

  This key specifies the minimum number of ongoing flows (i.e., created flows that have not yet finished) required for checking if they have reached the timeout or maximum flow time value. The value must be an integer. The default value is `2000`. This indicates that if the number of ongoing flows exceeds `2000`, the program will proceed to check all flows for timeout or maximum flow time.


* **capturer_updating_flows_min_value** [Optional]

  This key determines the minimum number of finished flows required to be added to the queue for feature extraction. The value must be an integer. The default value is `2000`. This means that if the number of finished flows exceeds `2000`, the program will move them to a separate list for the feature extractor.
  

* **max_flow_duration** [Optional]

  This key sets the maximum duration of a flow in seconds. The value must be an integer. The default value is `120,000`. It means if the flow duration exceeds `120,000` seconds, the program will terminate the flow and initiate a new one.


* **activity_timeout** [Optional]

  This key defines the flow activity timeout in seconds. The value must be an integer. The default value is `5000`. It means if `5000` seconds have elapsed since the last packet of the flow, the program will terminate the flow.


* **floating_point_unit** [Optional]

  This key specifies the floating point unit used for the feature extraction process. The value must be in the format: `.[UNIT]f`. The default value is `.4f`. This indicates that the feature values will be rounded to the fourth decimal place.


* **max_rows_number** [Optional]

  This key defines the maximum number of rows in the output CSV file. The value must be an integer. The default value is `900,000`. It means if there are more than `900,000` flows to be written in the CSV file, the program will close the current CSV file and create a new one for the remaining flows.


* **features_ignore_list** [Optional]

  This key specifies the features that you do not want to extract. The value must be a list of string values, where each string represents a feature name. The default value is an empty list. If you include a feature name in this list, the program will skip extracting that feature, and it will not appear in the output CSV file.


An example of a configuration file would be like this:

```json
{
    "pcap_file_address": "/mnt/c/dataset/my_pcap_file.pcap",
    "output_file_address": "./output-of-my_pcap_file.csv",
    "label": "Benign",
    "number_of_threads": 4,
    "feature_extractor_min_flows": 2500,
    "writer_min_rows": 1000,
    "read_packets_count_value_log_info": 1000000,
    "check_flows_ending_min_flows": 20000,
    "capturer_updating_flows_min_value": 5000,
    "dns_activity_timeout": 30,
    "max_flow_duration": 120000,
    "floating_point_unit": ".4f",
    "max_rows_number": 800000,
    "features_ignore_list": [
        "dns_whois_domain_name",
        "dns_domain_email",
        "dns_domain_registrar",
        "dns_domain_creation_date",
        "dns_domain_expiration_date",
        "dns_domain_age",
        "dns_domain_country",
        "dns_domain_dnssec",
        "dns_domain_dnssec",
        "dns_domain_address",
        "dns_domain_city",
        "dns_domain_state",
        "dns_domain_zipcode",
        "dns_domain_name_servers",
        "dns_domain_updated_date"
    ]
}
```


In general, we recommend adjusting the values of the following options: `number_of_threads`, `feature_extractor_min_flows`, `writer_min_rows`, `check_flows_ending_min_flows`, and `capturer_updating_flows_min_value`, based on your system configuration. This is particularly important if your PCAP file is large (usually more than 4 GB with over 1 million TCP packets), to optimize program efficiency.


## Argument Parser

You can use `-h` to see different options of the program.

To execute ALFlowLyzer, simply run the following command:

```bash
alflowlyzer -c YOUR_CONFIG_FILE
```

Replace `YOUR_CONFIG_FILE` with the path to your configuration file.


Moreover, this project has been successfully tested on Ubuntu 20.04, Ubuntu 22.04, Windows 10, and Windows 11. It should work on other versions of Ubuntu OS (or even Debian OS) as long as your system has the necessary Python3 packages (you can find the required packages listed in the `requirements.txt` file).


# Architecture


![](./Architecture.svg)

                
----

# Extracted Features
                
We currently have currently 130 features that are as follows:

1. Duration
1. Packets Numbers
1. Receiving Packets Numbers
1. Sending Packets Numbers
1. Successful packet numbers (HTTP packets only)
1. Successful packet rate (HTTP packets only)
1. Delta Start
1. Handshake Duration
1. Total Bytes
1. Receiving Bytes
1. Sending Bytes
1. Packets Rate
1. Receiving Packets Rate
1. Sending Packets Rate
1. Packets Len Rate
1. Receiving Len Packets Rate
1. Sending Len Packets Rate
1. Packets Len Min
1. Packets Len Max
1. Packets Len Mean
1. Packets Len Median
1. Packets Len Mode
1. Packets Len Standard Deviation
1. Packets Len Variance
1. Packets Len Coefficient of Variation
1. Packets Len Skewness
1. Receiving Packets Len Min
1. Receiving Packets Len Max
1. Receiving Packets Len Mean
1. Receiving Packets Len Median
1. Receiving Packets Len Mode
1. Receiving Packets Len Standard Deviation
1. Receiving Packets Len Variance
1. Receiving Packets Len Coefficient of Variation
1. Receiving Packets Len Skewness
1. Sending Packets Len Min
1. Sending Packets Len Max
1. Sending Packets Len Mean
1. Sending Packets Len Median
1. Sending Packets Len Mode
1. Sending Packets Len Standard Deviation
1. Sending Packets Len Variance
1. Sending Packets Len Coefficient of Variation
1. Sending Packets Len Skewness
1. Receiving Packets Delta Len Min
1. Receiving Packets Delta Len Max
1. Receiving Packets Delta Len Mean
1. Receiving Packets Delta Len Median
1. Receiving Packets Delta Len Standard Deviation
1. Receiving Packets Delta Len Variance
1. Receiving Packets Delta Len Mode
1. Receiving Packets Delta Len Coefficient of Variation
1. Receiving Packets Delta Len Skewness
1. Sending Packets Delta Len Min
1. Sending Packets Delta Len Max
1. Sending Packets Delta Len Mean
1. Sending Packets Delta Len Median
1. Sending Packets Delta Len Standard Deviation
1. Sending Packets Delta Len Variance
1. Sending Packets Delta Len Mode
1. Sending Packets Delta Len Coefficient of Variation
1. Sending Packets Delta Len Skewness
1. Receiving Packets Delta Time Max
1. Receiving Packets Delta Time Mean
1. Receiving Packets Delta Time Median
1. Receiving Packets Delta Time Standard Deviation
1. Receiving Packets Delta Time Variance
1. Receiving Packets Delta Time Mode
1. Receiving Packets Delta Time Coefficient of Variation
1. Receiving Packets Delta Time Skewness
1. Sending Packets Delta Time Min
1. Sending Packets Delta Time Max
1. Sending Packets Delta Time Mean
1. Sending Packets Delta Time Median
1. Sending Packets Delta Time Standard Deviation
1. Sending Packets Delta Time Variance
1. Sending Packets Delta Time Mode
1. Sending Packets Delta Time Coefficient of Variation
1. Sending Packets Delta Time Skewness

note: Delta features are about differences (time or length or anything else) between two 'consecutive' packets.

## DNS Related

1. Domain Name
1. WhoisDomainName
1. Top Level Domain
1. Second Level Domain
1. Domain Name Length
1. Sub Domain Name Length
1. Domain Name 1-Gram
1. Domain Name 2-Gram
1. Domain Name 3-Gram
1. Numerical Percentage
1. Character Distribution
1. Character Entropy
1. DomainEmail
1. DomainRegistrar
1. DomainCreationDate
1. DomainExpirationDate
1. DomainAge
1. DomainCountry
1. DomainDNSSEC
1. DomainOrganization
1. DomainAddress
1. DomainCity
1. DomainState
1. DomainZipcode
1. DomainNameServers
1. DomainUpdatedDate
1. Continuous Numeric Max Len
1. Continuous Alphabet Max Len
1. Continuous Consonant Max Len
1. Continuous Same Alphabet Max Len
1. Vowel Consonant Ratio
1. Conv Freq Vowel Consonant
1. Distinct TTL Values
1. TTL Values Min
1. TTL Values Max
1. TTL Values Mean
1. TTL Values Mode
1. TTL Values Variance
1. TTL Values Standard Deviation
1. TTL Values Median
1. TTL Values Skewness
1. TTL Values Coefficient of Variation
1. Distinct A Resource Records
1. Distinct NS Resource Records
1. Average Authority Resource Records
1. Average Additional Resource Records
1. Average Answer Resource Records
1. Query Resource Record Type
1. Answer Resource Record Type
1. Query Resource Record Class
1. Answer Resource Record Class


## Statistical Information Calculation

We use differnet libraries to calculate various mathematical equations. Below you can see the libraries and their brief definition based on their documentations:

+ [**statistics**](https://docs.python.org/3/library/statistics.html)

     This module provides functions for calculating mathematical statistics of numeric (Real-valued) data.

     The module is not intended to be a competitor to third-party libraries such as NumPy, SciPy, or proprietary full-featured statistics packages aimed at professional statisticians such as Minitab, SAS and Matlab. It is aimed at the level of graphing and scientific calculators.


+ [**scipy**](https://scipy.github.io/devdocs/tutorial/general.html)

     SciPy is a third-party library for scientific computing based on NumPy. It offers additional functionality compared to NumPy, including scipy.stats for statistical analysis. In this project, we use ['scipy.stats'](https://scipy.github.io/devdocs/tutorial/stats.html).



Nine mathematical functions are used to extract different features. You can see how those functions are calculated in the ALFlowLyzer below:

1. Min

      You know what it means :). The 'min' function (Python built-in) calculates the minimum value in a given list.

1. Max

      Same as min. The 'max' function (Python built-in) calculates the minimum value in a given list.

1. Mean

      The ['mean'](https://docs.python.org/3/library/statistics.html#statistics.mean) function from 'statistics' library (Python built-in) calculates the mean value of a given list. According to the library documentation:
        
      The arithmetic mean is the sum of the data divided by the number of data points. It is commonly called “the average”, although it is only one of many different mathematical averages. It is a measure of the central location of the data.
        
      This runs faster than the mean() function and it always returns a float. The data may be a sequence or iterable. If the input dataset is empty, raises a StatisticsError.



1. Median

      The ['median'](https://docs.python.org/3/library/statistics.html#statistics.median) function from 'statistics' library (Python built-in) calculates the mean value of a given list. According to the library documentation:
      
      Return the median (middle value) of numeric data, using the common “mean of middle two” method. If data is empty, StatisticsError is raised. data can be a sequence or iterable.

      The median is a robust measure of central location and is less affected by the presence of outliers. When the number of data points is odd, the middle data point is returned. When the number of data points is even, the median is interpolated by taking the average of the two middle values:


1. Variance

      The ['pvariance'](https://docs.python.org/3/library/statistics.html#statistics.pstdev) function from 'statistics' library (Python built-in) calculates the mean value of a given list. According to the library documentation:

      Return the population variance of data, a non-empty sequence or iterable of real-valued numbers. Variance, or second moment about the mean, is a measure of the variability (spread or dispersion) of data. A large variance indicates that the data is spread out; a small variance indicates it is clustered closely around the mean.
      
      Raises StatisticsError if data is empty.




1. Standard Deviation

      The ['pstdev'](https://docs.python.org/3/library/statistics.html#statistics.pstdev) function from 'statistics' library (Python built-in) calculates the mean value of a given list. According to the library documentation:

      Return the population standard deviation (the square root of the population variance). See pvariance() for arguments and other details.


1. Mode

      The ['mode'](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html) function from 'scipy.stats' library calculates the mode value of a given list. According to the library documentation, this function:
      
      Return an array of the modal (most common) value in the passed array.

      If there is more than one such value, only the smallest is returned. The bin-count for the modal bins is also returned.


1. Coefficient of Variation

      The ['variation'](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.variation.html) function from 'scipy.stats' library calculates the mode value of a given list. According to the library documentation, this function:
      
      The coefficient of variation is the standard deviation divided by the mean.
      
      There are several edge cases that are handled without generating a warning:

      + If both the mean and the standard deviation are zero, nan is returned.

      + If the mean is zero and the standard deviation is nonzero, inf is returned.

      + If the input has length zero (either because the array has zero length, or all the input values are nan and nan_policy is 'omit'), nan is returned.

      + If the input contains inf, nan is returned.

1. Skewness

      The ['skew'](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.skew.html) function from 'scipy.stats' library calculates the mode value of a given list. According to the library documentation, this function:
      
      For normally distributed data, the skewness should be about zero. For unimodal continuous distributions, a skewness value greater than zero means that there is more weight in the right tail of the distribution.
      
      The sample skewness is computed as the Fisher-Pearson coefficient of skewness, i.e.

      ![equation](https://latex.codecogs.com/svg.image?{\color{blue}&space;g_{1}=\frac{m_{3}}{m_{2}^{\frac{3}{2}}}})

      where

      ![equation](https://latex.codecogs.com/svg.image?{\color{blue}m_{i}=\frac{1}{N}\sum_n^N(x[n]-\overline{x})^{i}})
      
      is the biased sample ith central moment, and x- is the sample mean. If bias is False, the calculations are corrected for bias and the value computed is the adjusted Fisher-Pearson standardized moment coefficient, i.e.
      
      ![equation](https://latex.codecogs.com/svg.image?{\color{blue}G_{1}=\frac{k_{3}}{k_{2}^{\frac{3}{2}}}=\frac{\sqrt{N(N-1)}}{N-2}\frac{m_{3}}{m_{2}^{\frac{3}{2}}})      




----
                    
# Output


| flow_id  | 	timestamp  | 	src_ip  | 	src_port  | 	dst_ip  | 	dst_port  | 	protocol  | 	duration  | 	packets_numbers  | 	receiving_packets_numbers  | 	sending_packets_numbers  | handshake_duration | delta_start	| success_packets_numbers  | 	success_packets_rate  |  total_bytes  |  receiving_bytes  |  sending_bytes  | 	packets_rate  | 	receiving_packets_rate  | 	sending_packets_rate  |  packets_len_rate  |  receiving_packets_len_rate  |  sending_packets_len_rate  | 	min_packets_len  | 	max_packets_len  | 	mean_packets_len  | 	median_packets_len  | 	mode_packets_len  | 	standard_deviation_packets_len  | 	variance_packets_len  | 	coefficient_of_variation_packets_len  | 	skewness_packets_len  | 	min_receiving_packets_len  | 	max_receiving_packets_len  | 	mean_receiving_packets_len  | 	median_receiving_packets_len  | 	mode_receiving_packets_len  | 	standard_deviation_receiving_packets_len  | 	variance_receiving_packets_len  | 	coefficient_of_variation_receiving_packets_len  | 	skewness_receiving_packets_len  | 	min_sending_packets_len  | 	max_sending_packets_len  | 	mean_sending_packets_len  | 	median_sending_packets_len  | 	mode_sending_packets_len  | 	standard_deviation_sending_packets_len  | 	variance_sending_packets_len  | 	coefficient_of_variation_sending_packets_len  | 	skewness_sending_packets_len  | 	min_receiving_packets_delta_len  | 	max_receiving_packets_delta_len  | 	mean_receiving_packets_delta_len  | 	median_receiving_packets_delta_len  | 	standard_deviation_receiving_packets_delta_len  | 	variance_receiving_packets_delta_len  | 	mode_receiving_packets_delta_len  | 	coefficient_of_variation_receiving_packets_delta_len  | 	skewness_receiving_packets_delta_len  | 	min_sending_packets_delta_len  | 	max_sending_packets_delta_len  | 	mean_sending_packets_delta_len  | 	median_sending_packets_delta_len  | 	standard_deviation_sending_packets_delta_len  | 	variance_sending_packets_delta_len  | 	mode_sending_packets_delta_len  | 	coefficient_of_variation_sending_packets_delta_len  | 	skewness_sending_packets_delta_len  | 	max_receiving_packets_delta_time  | 	mean_receiving_packets_delta_time  | 	median_receiving_packets_delta_time  | 	standard_deviation_receiving_packets_delta_time  | 	variance_receiving_packets_delta_time  | 	mode_receiving_packets_delta_time  | 	coefficient_of_variation_receiving_packets_delta_time  | 	skewness_sreceiving_packets_delta_time  | 	min_sending_packets_delta_time  | 	max_sending_packets_delta_time  | 	mean_sending_packets_delta_time  | 	median_sending_packets_delta_time  | 	standard_deviation_sending_packets_delta_time  | 	variance_sending_packets_delta_time  | 	mode_sending_packets_delta_time  | 	coefficient_of_variation_sending_packets_delta_time  | 	skewness_sending_packets_delta_time  | domain_name | top_level_domain | second_level_domain | domain_name_length | subdomain_name_length | uni_gram_domain_name | bi_gram_domain_name | tri_gram_domain_name | numerical_percentage | character_distribution | character_entropy | max_continuous_numeric_len | max_continuous_aphabet_len | max_continuous_consonants_len | max_continuous_same_alphabet_len | vowels_consonant_ratio | conv_freq_vowels_consonants | distinct_ttl_values | ttl_values_min | ttl_values_max | ttl_values_mean | ttl_values_mode | ttl_values_variance | ttl_values_standard_deviation | ttl_values_median | ttl_values_skewness | ttl_values_coefficient_of_variation | distinct_A_records | distinct_NS_records | average_authority_resource_records | average_additional_resource_records | average_answer_resource_records | query_resource_record_type | ans_resource_record_type | query_resource_record_class | ans_resource_record_class |
| :------------:| :----------------: | :----------------: | :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: | :------------: | :----------------: | :----------------: | :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: | :------------: | :----------------: | :----------------: | :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: | :----------------: | :----------------: | :------------:| :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: | :----------------: |
| 2022-04-15 01:00:59_192.168.116.100_42206_109.206.255.42_443  | 	4/15/2022 1:00  | 	192.168.116.100  | 	42206  | 	109.206.255.42  | 	443  | 	HTTPS  | 	187.146098  | 	457  | 	163  | 	294  | 0.002181 | 0.000112 | 	0  | 	0  |  368700  |  15074  |  353626  | 	2.441942444  | 	0.870978112  | 	1.570983276  |  1970.11855411487  |  80.5467733413584  |  1889.5936464734  | 	66  | 	1517  | 	806.7833698  | 	1090  | 	1514  | 	696.4427299  | 	485032.476  | 	0.863233869  | 	-0.02915255  | 	66  | 	850  | 	92.47852761  | 	66  | 	66  | 	86.10055025  | 	7413.304754  | 	0.931032884  | 	5.745042137  | 	66  | 	1517  | 	1202.809524  | 	1514  | 	1514  | 	556.879545  | 	310114.8277  | 	0.462982321  | 	-1.372465268  | 	-784  | 	692  | 	-0.049382716  | 	0  | 	115.3815358  | 	13312.8988  | 	0  | 	-2336.476099  | 	-0.574504437  | 	-1283  | 	1398  | 	-0.027303754  | 	0  | 	366.8574496  | 	134584.3883  | 	0  | 	-13436.15409  | 	0.361252195  | 	45.05993915  | 	1.155221727  | 	0.00019002  | 	6.983534339  | 	48.76975187  | 	0.00011301  | 	6.045189573  | 	6.106573202  | 	0  | 	45.05982494  | 	0.638716519  | 	0.000112057  | 	5.22443504  | 	27.29472149  | 	5.6982E-05  | 	8.17958341  | 	8.356739983  | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow |
| 2022-04-15 01:05:39_192.168.116.100_58528_192.168.91.24_80 | 4/15/2022 1:05 | 192.168.116.100 | 58528 | 192.168.91.24 | 80 | HTTP | 7.875475 | 1050 | 281 | 769 | 0.001688 | 0.000106 | 13 | 1.650694085 | 1198900 | 36130 | 1162770 | 133.3252915 | 35.68119399 | 97.66550239  |  152232.087588367  |  4587.76348371369  |  147675.57374355  | 66 | 10202 | 1141.809524 | 1514 | 1514 | 810.3565446 | 656677.7294 | 0.709712546 | 1.938364541 | 66 | 1428 | 128.5765125 | 66 | 66 | 240.7908131 | 57980.21568 | 1.872743385 | 3.891267082 | 66 | 10202 | 1512.054616 | 1514 | 1514 | 602.6786735 | 363221.5835 | 0.398582609 | 6.298889431 | -1362 | 1362 | -0.028571429 | 0 | 340.8741063 | 116195.1563 | 0 | -11930.59372 | -0.066420757 | -8688 | 8688 | -0.010416667 | 0 | 701.4665366 | 492055.302 | 0 | -67340.78751 | -0.555146197 | 2.694911957 | 0.028126061 | 0.000115871 | 0.202381878 | 0.040958425 | 0.00011301 | 7.19552868 | 11.15603825 | 0 | 2.695833921 | 0.010252362 | 6.98566E-05 | 0.12326028 | 0.015193097 | 6.69956E-05 | 12.02262252 | 18.48471894 | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow |
| 2022-04-15 01:00:11_192.168.116.100_56471_192.168.92.11_53 | 4/15/2022 1:00 | 192.168.116.100 | 56471 | 192.168.92.11 | 53 | DNS | 0.002526 | 2 | 1 | 1 | not a tcp connection | not a tcp connection | 0 | 0 | 220 | 102 | 118 | 791.7656374 | 0 | 0 | 87094.2201108471 | 0 | 0 | 102 | 118 | 110 | 110 | 102 | 8 | 64 | 0.072727273 | 0 | 102 | 102 | 102 | 102 | 102 | 0 | 0 | 0 | 0 | 118 | 118 | 118 | 118 | 118 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | content-autofill.googleapis.com. | .com | .googleapis.com | 32 | 16 | ['c', 'o', 'n', 't', 'e', 'n', 't', '-', 'a', 'u', 't', 'o', 'f', 'i', 'l', 'l', '.', 'g', 'o', 'o', 'g', 'l', 'e', 'a', 'p', 'i', 's', '.', 'c', 'o', 'm', '.'] | ['co', 'on', 'nt', 'te', 'en', 'nt', 't-', '-a', 'au', 'ut', 'to', 'of', 'fi', 'il', 'll', 'l.', '.g', 'go', 'oo', 'og', 'gl', 'le', 'ea', 'ap', 'pi', 'is', 's.', '.c', 'co', 'om', 'm.'] | ['con', 'ont', 'nte', 'ten', 'ent', 'nt-', 't-a', '-au', 'aut', 'uto', 'tof', 'ofi', 'fil', 'ill', 'll.', 'l.g', '.go', 'goo', 'oog', 'ogl', 'gle', 'lea', 'eap', 'api', 'pis', 'is.', 's.c', '.co', 'com', 'om.'] | 0 | {'m': 1, 's': 1, 'p': 1, '.': 3, 'g': 2, 'l': 3, 'o': 5, '-': 1, 't': 3, 'i': 2, 'a': 2, 'f': 1, 'n': 2, 'c': 2, 'e': 2, 'u': 1} | 3.81642803184602 | 0 | 10 | 2 | 2 | 0.75 | 0.53125 | 2 | 0 | 415 | 207.5 | 0 | 43056.25 | 207.5 | 207.5 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | [1, 1] | [0, 1] | [1, 1] | [0, 1] |
| 2022-04-15 01:01:40_192.168.116.100_43244_192.168.119.112_22 | 4/15/2022 1:01 | 192.168.116.100 | 43244 | 192.168.119.112 | 22 | Others | 6.917505 | 23283 | 7452 | 15831 | 0.00093 | 0.000222 | 0 | 0 | 24671240 | 501761 | 24169479 | 3365.808915 | 1077.302684 | 2288.839353 | 3566493.98880087 | 72537.3687561404 | 3494413.15581659 | 66 | 36266 | 1059.624619 | 1514 | 1514 | 765.659792 | 586234.917 | 0.722576447 | 6.898108476 | 66 | 1578 | 67.33239399 | 66 | 66 | 20.63231412 | 425.6923859 | 0.306424782 | 60.05231415 | 66 | 36266 | 1526.718401 | 1514 | 1514 | 424.6387625 | 180318.0786 | 0.278138236 | 60.85177157 | -1512 | 1512 | -0.001073681 | 0 | 29.21008551 | 853.2290956 | 0 | -27205.54339 | -0.001048411 | -31856 | 34752 | -0.00050537 | 0 | 567.7554589 | 322346.2611 | 0 | -1123446.114 | 3.715976314 | 4.359194994 | 0.000928369 | 0.000169992 | 0.051381806 | 0.00264009 | 0.000170946 | 55.34633046 | 82.30143017 | 0 | 4.317461967 | 0.00043693 | 6.19888E-05 | 0.034980458 | 0.001223632 | 5.6982E-05 | 80.05959085 | 119.424366 | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow | not a dns flow |


# Copyright (c) 2024

For citation in your works and also understanding ALFlowLyzer completely, you can find below published papers:

- “Unveiling malicious DNS behavior profiling and generating benchmark dataset through application layer traffic analysis”, MohammadMoein Shafi, Arash Habibi Lashkari, and Hardhik Mohanty

# Contributing

Any contribution is welcome in the form of pull requests.


# Project Team members 

* [**Arash Habibi Lashkari:**](http://ahlashkari.com/index.asp) Founder and supervisor

* [**Moein Shafi:**](https://github.com/moein-shafi) Graduate student, Researcher and developer - York University

* [**Hardik Mohanty:**](https://github.com/hardhik-99) Mitacs Global Research Internship (GRI), Researcher and developer - York University


# Acknowledgement
This project has been made possible through funding from the Natural Sciences and Engineering Research Council of Canada — NSERC (#RGPIN-2020-04701), Canada Research Chair (Tier II) - (#CRC-2021-00340) to Arash Habibi Lashkari and Mitacs Global Research Internship (MGRI) program for summer student.

                    

----

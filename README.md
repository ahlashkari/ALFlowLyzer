# AppFlowMeter
TODO: update these values:
![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg)


# Table of Contents

- [Installation](#installation)
- [Architecture](#architecture)
- [Extracted Features](#extracted-features)
  * [Statistical Information Calculation](#statistical-information-calculation)
- [Output](#output)


# Installation

You must install the requirements in your system before you can begin installing or running anything. To do so, you can easily run this command:

```bash
sudo pip3 install -r requirements.txt
```

You are now ready to install AppFlowMeter. In order to do so, you should run this command, which will install the AppFlowMeter package in your system:

```bash
sudo python3 setup.py install
```

Finally, to execute the program, run this command:

```bash
sudo app-flow-meter
```
Also, you can use `-h` to see different options of the program.

Moreover, this project has been successfully tested on Ubuntu 20.04. It should work on other versions of Ubuntu OS (or even Debian OS) as long as your system has the necessary python3 packages (you can see the required packages in the `requirements.txt` file).

TODO: after adding arg parser, explain different options here.

TODO: after adding config file, explain how to use it here.


# Architecture


![](./Architecture.svg)

                
----

# Extracted Features
                
We have currenlty 78 features that are as follows:
1. Duration
1. Packets Numbers
1. Receiving Packets Numbers
1. Sending Packets Numbers
1. Successful Packets Numbers (HTTP packets only)
1. Successful Packets Rate (HTTP packets only)
1. Delta Start
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

## Statistical Information Calculation

We use differnet libraries to calculate various mathematical equations. Below you can see the libraries and their brief definition based on their documentations:

+ [**statistics**](https://docs.python.org/3/library/statistics.html)

     This module provides functions for calculating mathematical statistics of numeric (Real-valued) data.

     The module is not intended to be a competitor to third-party libraries such as NumPy, SciPy, or proprietary full-featured statistics packages aimed at professional statisticians such as Minitab, SAS and Matlab. It is aimed at the level of graphing and scientific calculators.


+ [**scipy**](https://scipy.github.io/devdocs/tutorial/general.html)

     SciPy is a third-party library for scientific computing based on NumPy. It offers additional functionality compared to NumPy, including scipy.stats for statistical analysis. In this project, we use ['scipy.stats'](https://scipy.github.io/devdocs/tutorial/stats.html).



TODO: for all functions, use scipy library instead of statistics (because it is faster).


Nine mathematical functions are used to extract different features. You can see how those functions are calculated in the AppFlowMeter below:

1. Min

      You know what it means :). The 'min' function (Python built-in) calculates the minimum value in a given list.

1. Max

      Same as min. The 'max' function (Python built-in) calculates the minimum value in a given list.

1. Mean

      The ['mean'](https://docs.python.org/3/library/statistics.html#statistics.mean) function from 'statistics' library (Python built-in) calculates the mean value of a given list. According to the library documentation:
        
      The arithmetic mean is the sum of the data divided by the number of data points. It is commonly called “the average”, although it is only one of many different mathematical averages. It is a measure of the central location of the data.

      TODO: use 'fmean' instead of mean (it is new in python 3.8). According to the library documentation:
        
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


| flow_id  | 	timestamp  | 	src_ip  | 	src_port  | 	dst_ip  | 	dst_port  | 	protocol  | 	duration  | 	packets_numbers  | 	receiving_packets_numbers  | 	sending_packets_numbers  | 	success_packets_numbers  | 	success_packets_rate  | delta_start | total_bytes  |  receiving_bytes  |  sending_bytes  | 	packets_rate  | 	receiving_packets_rate  | 	sending_packets_rate  |  packets_len_rate  |  receiving_packets_len_rate  |  sending_packets_len_rate  | 	min_packets_len  | 	max_packets_len  | 	mean_packets_len  | 	median_packets_len  | 	mode_packets_len  | 	standard_deviation_packets_len  | 	variance_packets_len  | 	coefficient_of_variation_packets_len  | 	skewness_packets_len  | 	min_receiving_packets_len  | 	max_receiving_packets_len  | 	mean_receiving_packets_len  | 	median_receiving_packets_len  | 	mode_receiving_packets_len  | 	standard_deviation_receiving_packets_len  | 	variance_receiving_packets_len  | 	coefficient_of_variation_receiving_packets_len  | 	skewness_receiving_packets_len  | 	min_sending_packets_len  | 	max_sending_packets_len  | 	mean_sending_packets_len  | 	median_sending_packets_len  | 	mode_sending_packets_len  | 	standard_deviation_sending_packets_len  | 	variance_sending_packets_len  | 	coefficient_of_variation_sending_packets_len  | 	skewness_sending_packets_len  | 	min_receiving_packets_delta_len  | 	max_receiving_packets_delta_len  | 	mean_receiving_packets_delta_len  | 	median_receiving_packets_delta_len  | 	standard_deviation_receiving_packets_delta_len  | 	variance_receiving_packets_delta_len  | 	mode_receiving_packets_delta_len  | 	coefficient_of_variation_receiving_packets_delta_len  | 	skewness_receiving_packets_delta_len  | 	min_sending_packets_delta_len  | 	max_sending_packets_delta_len  | 	mean_sending_packets_delta_len  | 	median_sending_packets_delta_len  | 	standard_deviation_sending_packets_delta_len  | 	variance_sending_packets_delta_len  | 	mode_sending_packets_delta_len  | 	coefficient_of_variation_sending_packets_delta_len  | 	skewness_sending_packets_delta_len  | 	max_receiving_packets_delta_time  | 	mean_receiving_packets_delta_time  | 	median_receiving_packets_delta_time  | 	standard_deviation_receiving_packets_delta_time  | 	variance_receiving_packets_delta_time  | 	mode_receiving_packets_delta_time  | 	coefficient_of_variation_receiving_packets_delta_time  | 	skewness_sreceiving_packets_delta_time  | 	min_sending_packets_delta_time  | 	max_sending_packets_delta_time  | 	mean_sending_packets_delta_time  | 	median_sending_packets_delta_time  | 	standard_deviation_sending_packets_delta_time  | 	variance_sending_packets_delta_time  | 	mode_sending_packets_delta_time  | 	coefficient_of_variation_sending_packets_delta_time  | 	skewness_sending_packets_delta_time  |
| :------------:| :----------------: | :----------------: | :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: | :------------: | :----------------: | :----------------: | :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: | :------------: | :----------------: | :----------------: | :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |
| 2021-12-15 16:35:00--128.14.134.170--57468--198.71.247.91--80	| 15-12-2021 16:35	| 128.14.134.170	| 57468	| 198.71.247.91	| 80	| HTTP	| 5.162805	| 10	| 6	| 4	| 1	| 0	| 0.011593	| 1159	| 609	| 550	| 1.936931571	| 1.162158943	| 0.797287469	| 224.4903691	| 117.9591327	| 109.6270269	| 66	| 344	| 115.9	| 66	| 66	| 97.23008794	| | | 9453.69	| 0.838913615	| 1.59994368	| 66	| 271	| 101.5	| 66	| 66	| 75.85897003	| 5754.583333	| 0.747379015	| 1.782982702	| 66	| 344	| 137.5	| 70	| 66	| 119.2675564	| 14224.75	| 0.86740041	| 1.15212042	| -205	| 205	| -1.6	| 0	| 129.692868	| 16820.24	| 0	| -81.05804248	| 0.036965453	| -278	| 278	| -2.666666667	| -8	227.0173757	| 51536.88889	| -278	| -85.1315159	| 0.035226627	| 5.041104078	| 1.032561016	| 0.012708902	| 2.004574787	| 4.018320079	| 5.00679E-05	| 1.941362066	| 1.498872048	| | | 0.001091003	| 5.004333973	| 1.672337055	| 0.011586189	| 2.356081511	| 5.551120088	| 0.001091003	| 1.408855651	| 0.707096258
| 2021-12-15 16:57:35--139.162.242.152--57268--198.71.247.91--80	| 15-12-2021 16:57	| 139.162.242.152	| 57268	| 198.71.247.91	| 80	| HTTP	| 0.292063	| 9	| 5	| 4	| 1	| 0	| 0.144898	| 1060	| 510	| 550	| 30.81526931	| 17.1315014	| 13.70069463	| 3629.353941	| 1747.413143	| 1883.845511	| 66	| 344	| 117.7777778	| 66	| 66	| 95.95575112	| 9207.506173	| 0.814718642	| 1.566097906	| 66	| 238	| 102	| 66	| 66	| 68.07055164	| 4633.6	| 0.667358349	| 1.492358045	| 66	| 344	| 137.5	| 70	| 66	| 119.2675564	| 14224.75	| 0.86740041	| 1.15212042	| -172	| 172	| -2	| -4	| 121.6716894	| 14804	| -172	| -60.8358447	| 0.049246411	| -278	| 278	| -2.666666667	| -8	| 227.0173757	| 51536.88889	| -278	| -85.1315159	| 0.035226627	| 0.145081043	| 0.072965026	| 0.072958589	| 0.071595383	| 0.005125899	| 0.000861883	| 0.981228778	| 3.8884E-06	| 0.001055002	| 0.146011114	| 0.097318649	| 0.144889832	| 0.068070217	| 0.004633554	| 0.001055002	| 0.699457065	| -0.706962883
| 2021-12-15 16:57:48--172.70.135.112--37220--198.71.247.91--80	| 15-12-2021 16:57	| 172.70.135.112	| 37220	| 198.71.247.91	| 80	| HTTP	| 8.922069	| 72	| 45	| 27	| 3	| 0.336244878	| 0.061763	| 25298	| 13918	| 11380	| 8.069877066	| 5.043673166	| 3.047376891	| 2835.440972	| 1559.952069	| 1284.412927	| 54	| 611	| 351.3611111	| 549	| 54	| 254.1804535	| 64607.70293	| 0.72341658	| -0.268009689	| 54	| 611	| 309.2888889	| 54	| 54	| 272.5015492	| 74257.09432	| 0.881058321	| 0.135988233	| 54	| 549	| 421.4814815	| 549	| 549	| 201.6392764	| 40658.39781	| 0.478406016	| -1.155812095	| -557	| 557	| -0.272727273	| -6	| 534.034999	| 285193.3802	| -552	| -1958.12833	| 0.001531818	| -495	| 495	| -0.461538462	| 0	| 238.3933774	| 56831.40237	| 0	| -516.5189843	| 0.005803213	| 4.962744951	| 0.202774297	| 0.062247515	| 0.73029494	| 0.533330699	| 2.7895E-05	| 3.601516319	| 6.28727802	| 0.000276089	| 5.003100872	| 0.340772271	| 0.162039995	| 0.939850353	| 0.883318686	| 0.000276089 | 2.758001259 | 4.680181841
| 2021-12-15 17:01:01--36.37.151.96--20010--198.71.247.91--80	| 15-12-2021 17:01	| 36.37.151.96	| 20010	| 198.71.247.91	| 80	| HTTP	| 0.418838	| 9	| 5	| 4	| 1	| 0	| 0.208419	| 1073	| 523	| 550	| 21.48802162	| 11.94683182	| 9.551417669	| 2561.849689	| 1249.638608	| 1313.31993	| 66	| 344	| 119.2222222	| 66	| 66	| 97.8340747	| 9571.506173	| 0.820602677	| 1.507696728	| 66	| 251	| 104.6	| 66	| 66	| 73.26554443	| 5367.84	| 0.700435415	| 1.493395232	| 66	| 344	| 137.5	| 70	| 66	| 119.2675564	| 14224.75	| 0.86740041	| 1.15212042	| -185	| 185	| -2	| -4	| 130.8606129	| 17124.5	| -185	| -65.43030643	| 0.045796763	| -278	| 278	| -2.666666667	| -8	| 227.0173757	| 51536.88889	| -278	| -85.1315159	| 0.035226627	| 0.209882021	| 0.104630232	| 0.104209423	| 0.104241754	| 0.010866343	| 0.00022006	| 0.99628714	| 0.000137494	| 0.001383066	| 0.208903074	| 0.13959535	| 0.208499908	| 0.097730981	| 0.009551345	| 0.001383066	| 0.700101986	| -0.707097756
                    

----


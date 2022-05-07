# AppFlowMeter
![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg)


**Table of Contents**

- [Installation](#installation)
  * [Requirements](#requirements)
- [Architecture](#architecture)
- [Extracted Features](#extracted-features)
  * [Statistical Information Calculation](#statistical-information-calculation)
- [Output](#output)


# Installation

## Requirements
```bash
sudo pip3 install -r requirements.txt
```
```bash
sudo python3 setup.py install
```
```bash
app-flow-meter
```


# Architecture

![](https://github.com/ahlashkari/AppFlowMeter/blob/features/10-update-readme-file/Architecture.svg)

                
----

# Extracted Features
                
We have currenlty 80 features that are as follows:
+ Item A
+ Item B
+ Item C

## Statistical Information Calculation
ss



----
                    
# Output


| flow_id  | 	timestamp  | 	src_ip  | 	src_port  | 	dst_ip  | 	dst_port  | 	protocol  | 	duration  | 	packets_numbers  | 	receiving_packets_numbers  | 	sending_packets_numbers  | 	success_packets_numbers  | 	success_packets_rate  | 	packets_rate  | 	receiving_packets_rate  | 	sending_packets_rate  | 	min_packets_len  | 	max_packets_len  | 	mean_packets_len  | 	median_packets_len  | 	mode_packets_len  | 	standard_deviation_packets_len  | 	variance_packets_len  | 	coefficient_of_variation_packets_len  | 	skewness_packets_len  | 	min_receiving_packets_len  | 	max_receiving_packets_len  | 	mean_receiving_packets_len  | 	median_receiving_packets_len  | 	mode_receiving_packets_len  | 	standard_deviation_receiving_packets_len  | 	variance_receiving_packets_len  | 	coefficient_of_variation_receiving_packets_len  | 	skewness_receiving_packets_len  | 	min_sending_packets_len  | 	max_sending_packets_len  | 	mean_sending_packets_len  | 	median_sending_packets_len  | 	mode_sending_packets_len  | 	standard_deviation_sending_packets_len  | 	variance_sending_packets_len  | 	coefficient_of_variation_sending_packets_len  | 	skewness_sending_packets_len  | 	min_receiving_packets_delta_len  | 	max_receiving_packets_delta_len  | 	mean_receiving_packets_delta_len  | 	median_receiving_packets_delta_len  | 	standard_deviation_receiving_packets_delta_len  | 	variance_receiving_packets_delta_len  | 	mode_receiving_packets_delta_len  | 	coefficient_of_variation_receiving_packets_delta_len  | 	skewness_receiving_packets_delta_len  | 	min_sending_packets_delta_len  | 	max_sending_packets_delta_len  | 	mean_sending_packets_delta_len  | 	median_sending_packets_delta_len  | 	standard_deviation_sending_packets_delta_len  | 	variance_sending_packets_delta_len  | 	mode_sending_packets_delta_len  | 	coefficient_of_variation_sending_packets_delta_len  | 	skewness_sending_packets_delta_len  | 	max_receiving_packets_delta_time  | 	mean_receiving_packets_delta_time  | 	median_receiving_packets_delta_time  | 	standard_deviation_receiving_packets_delta_time  | 	variance_receiving_packets_delta_time  | 	mode_receiving_packets_delta_time  | 	coefficient_of_variation_receiving_packets_delta_time  | 	skewness_sreceiving_packets_delta_time  | 	min_sending_packets_delta_time  | 	max_sending_packets_delta_time  | 	mean_sending_packets_delta_time  | 	median_sending_packets_delta_time  | 	standard_deviation_sending_packets_delta_time  | 	variance_sending_packets_delta_time  | 	mode_sending_packets_delta_time  | 	coefficient_of_variation_sending_packets_delta_time  | 	skewness_sending_packets_delta_time  |
| :------------:| :----------------: | :----------------: | :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: | :------------: | :----------------: | :----------------: | :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: | :------------: | :----------------: | :----------------: | :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |  :----------------: |
| 2022-04-15 01:00:59--192.168.116.100--42206--109.206.255.42--443  | 	4/15/2022 1:00  | 	192.168.116.100  | 	42206  | 	109.206.255.42  | 	443  | 	HTTPS  | 	187.146098  | 	457  | 	163  | 	294  | 	0  | 	0  | 	2.441942444  | 	0.870978112  | 	1.570983276  | 	66  | 	1517  | 	806.7833698  | 	1090  | 	1514  | 	696.4427299  | 	485032.476  | 	0.863233869  | 	-0.02915255  | 	66  | 	850  | 	92.47852761  | 	66  | 	66  | 	86.10055025  | 	7413.304754  | 	0.931032884  | 	5.745042137  | 	66  | 	1517  | 	1202.809524  | 	1514  | 	1514  | 	556.879545  | 	310114.8277  | 	0.462982321  | 	-1.372465268  | 	-784  | 	692  | 	-0.049382716  | 	0  | 	115.3815358  | 	13312.8988  | 	0  | 	-2336.476099  | 	-0.574504437  | 	-1283  | 	1398  | 	-0.027303754  | 	0  | 	366.8574496  | 	134584.3883  | 	0  | 	-13436.15409  | 	0.361252195  | 	45.05993915  | 	1.155221727  | 	0.00019002  | 	6.983534339  | 	48.76975187  | 	0.00011301  | 	6.045189573  | 	6.106573202  | 	0  | 	45.05982494  | 	0.638716519  | 	0.000112057  | 	5.22443504  | 	27.29472149  | 	5.6982E-05  | 	8.17958341  | 	8.356739983  |
| 2022-04-15 01:05:39--192.168.116.100--58528--192.168.91.24--80 | 4/15/2022 1:05 | 192.168.116.100 | 58528 | 192.168.91.24 | 80 | HTTP | 7.875475 | 1050 | 281 | 769 | 13 | 1.650694085 | 133.3252915 | 35.68119399 | 97.66550239 | 66 | 10202 | 1141.809524 | 1514 | 1514 | 810.3565446 | 656677.7294 | 0.709712546 | 1.938364541 | 66 | 1428 | 128.5765125 | 66 | 66 | 240.7908131 | 57980.21568 | 1.872743385 | 3.891267082 | 66 | 10202 | 1512.054616 | 1514 | 1514 | 602.6786735 | 363221.5835 | 0.398582609 | 6.298889431 | -1362 | 1362 | -0.028571429 | 0 | 340.8741063 | 116195.1563 | 0 | -11930.59372 | -0.066420757 | -8688 | 8688 | -0.010416667 | 0 | 701.4665366 | 492055.302 | 0 | -67340.78751 | -0.555146197 | 2.694911957 | 0.028126061 | 0.000115871 | 0.202381878 | 0.040958425 | 0.00011301 | 7.19552868 | 11.15603825 | 0 | 2.695833921 | 0.010252362 | 6.98566E-05 | 0.12326028 | 0.015193097 | 6.69956E-05 | 12.02262252 | 18.48471894 |
| 2022-04-15 01:00:11--192.168.116.100--56471--192.168.92.11--53 | 4/15/2022 1:00 | 192.168.116.100 | 56471 | 192.168.92.11 | 53 | DNS | 0.002526 | 2 | 1 | 1 | 0 | 0 | 791.7656374 | 0 | 0 | 102 | 118 | 110 | 110 | 102 | 8 | 64 | 0.072727273 | 0 | 102 | 102 | 102 | 102 | 102 | | 0 | 0 | 0 | 0 | 118 | 118 | 118 | 118 | 118 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2022-04-15 01:01:40--192.168.116.100--43244--192.168.119.112--22 | 4/15/2022 1:01 | 192.168.116.100 | 43244 | 192.168.119.112 | 22 | Others | 6.917505 | 23283 | 7452 | 15831 | 0 | 0 | 3365.808915 | 1077.302684 | 2288.839353 | 66 | 36266 | 1059.624619 | 1514 | 1514 | 765.659792 | 586234.917 | 0.722576447 | 6.898108476 | 66 | 1578 | 67.33239399 | 66 | 66 | 20.63231412 | 425.6923859 | 0.306424782 | 60.05231415 | 66 | 36266 | 1526.718401 | 1514 | 1514 | 424.6387625 | 180318.0786 | 0.278138236 | 60.85177157 | -1512 | 1512 | -0.001073681 | 0 | 29.21008551 | 853.2290956 | 0 | -27205.54339 | -0.001048411 | -31856 | 34752 | -0.00050537 | 0 | 567.7554589 | 322346.2611 | 0 | -1123446.114 | 3.715976314 | 4.359194994 | 0.000928369 | 0.000169992 | 0.051381806 | 0.00264009 | 0.000170946 | 55.34633046 | 82.30143017 | 0 | 4.317461967 | 0.00043693 | 6.19888E-05 | 0.034980458 | 0.001223632 | 5.6982E-05 | 80.05959085 | 119.424366 |
                    

----


"""
    分别完成csv/questdb的记录
    
"""
from datetime import datetime#
import os#
import csv#

def csv_put_contents(file, data, labels=None, file_append=True):
    open_mode = 'a+' if file_append is True else 'w'
    try:
        #判断文件是否存在并且加入表头
        need_header = not os.path.isfile(file) if isinstance(labels,list) else False
        with open(file, mode=open_mode, newline='') as f:
            writer = csv.writer(f)
            if need_header:
                writer.writerow(labels)
            
            writer.writerows(data)
    except IOError:
        print("I/O error")
        return False

    return len(data)
#END csv_put_contents

def main():
    labels = ['ts','open','high','low','close','volume']
    t_data = [[1609430400000, 773.63, 774.23, 773.63, 773.65, 1093.0], [1609430460000, 773.18, 773.63, 770.85, 770.85, 1058.0], [1609430520000, 770.84, 770.97, 769.81, 770.25, 1382.0], [1609430580000, 769.97, 770.4, 769.97, 770.25, 1054.0], [1609430640000, 769.82, 770.66, 769.3, 769.99, 340.0], [1609430700000, 769.96, 771.73, 769.96, 771.73, 183.0], [1609430760000, 771.82, 772.36, 771.43, 771.69, 502.0], [1609430820000, 771.44, 771.8, 770.76, 770.85, 413.0], [1609430880000, 770.8, 771.52, 770.3, 771.52, 913.0], [1609430940000, 771.75, 772.31, 771.31, 771.72, 351.0], [1609431000000, 771.61, 771.61, 770.3, 771.27, 308.0], [1609431060000, 770.52, 771.19, 770.21, 771.02, 223.0], [1609431120000, 771.14, 771.82, 770.77, 770.77, 476.0], [1609431180000, 770.6, 770.89, 769.84, 770.78, 716.0], [1609431240000, 770.37, 771.48, 770.37, 771.48, 397.0], [1609431300000, 771.1, 771.1, 769.99, 769.99, 549.0], [1609431360000, 769.22, 769.22, 767.99, 768.8, 634.0], [1609431420000, 769.31, 769.31, 768.3, 769.0, 965.0], [1609431480000, 769.38, 769.85, 768.84, 768.84, 871.0], [1609431540000, 769.0, 770.6, 768.68, 770.6, 371.0], [1609431600000, 770.45, 772.24, 770.38, 772.24, 481.0], [1609431660000, 770.91, 771.81, 770.91, 771.73, 204.0], [1609431720000, 771.12, 771.76, 770.55, 771.69, 281.0], [1609431780000, 771.11, 771.93, 771.11, 771.41, 613.0], [1609431840000, 771.23, 771.87, 771.23, 771.63, 546.0], [1609431900000, 771.6, 772.54, 771.11, 772.54, 278.0], [1609431960000, 772.18, 772.18, 771.56, 772.08, 310.0], [1609432020000, 772.18, 772.18, 771.38, 771.6, 886.0], [1609432080000, 771.55, 771.55, 770.69, 770.69, 180.0], [1609432140000, 770.93, 770.93, 769.67, 769.67, 246.0], [1609432200000, 770.13, 770.36, 769.66, 770.32, 251.0], [1609432260000, 770.04, 770.37, 769.5, 769.61, 170.0], [1609432320000, 769.86, 769.98, 768.89, 768.89, 386.0], [1609432380000, 768.89, 770.2, 768.77, 769.24, 361.0], [1609432440000, 769.15, 769.86, 769.09, 769.52, 169.0], [1609432500000, 768.99, 769.92, 768.64, 769.02, 893.0], [1609432560000, 769.15, 769.15, 768.39, 768.78, 303.0], [1609432620000, 768.26, 769.16, 768.26, 768.86, 334.0], [1609432680000, 768.74, 769.35, 768.59, 769.11, 404.0], [1609432740000, 768.6, 769.09, 766.98, 768.31, 896.0], [1609432800000, 768.14, 768.14, 767.19, 767.67, 421.0], [1609432860000, 767.57, 768.25, 766.47, 766.79, 567.0], [1609432920000, 766.91, 766.96, 766.49, 766.74, 669.0], [1609432980000, 767.0, 767.22, 766.7, 767.11, 146.0], [1609433040000, 767.03, 767.64, 766.29, 766.29, 433.0], [1609433100000, 766.42, 767.14, 765.98, 766.6, 424.0], [1609433160000, 765.31, 766.1, 763.89, 765.9, 1366.0], [1609433220000, 765.89, 766.0, 765.13, 765.22, 199.0], [1609433280000, 765.19, 765.49, 763.63, 763.63, 674.0], [1609433340000, 763.03, 764.36, 762.52, 764.1, 1456.0], [1609433400000, 764.21, 764.64, 763.69, 763.8, 486.0], [1609433460000, 763.67, 763.67, 761.63, 761.63, 1390.0], [1609433520000, 761.59, 762.88, 761.59, 762.62, 538.0], [1609433580000, 762.41, 764.28, 762.41, 764.28, 550.0], [1609433640000, 764.62, 764.62, 763.6, 763.67, 676.0], [1609433700000, 764.35, 764.35, 763.68, 764.24, 214.0], [1609433760000, 764.66, 764.85, 763.83, 764.64, 1010.0], [1609433820000, 764.87, 764.87, 763.16, 763.36, 390.0], [1609433880000, 762.98, 763.94, 762.8, 763.53, 198.0], [1609433940000, 763.46, 763.91, 763.07, 763.74, 273.0], [1609434000000, 763.87, 764.01, 762.68, 763.94, 312.0], [1609434060000, 764.25, 764.84, 764.2, 764.71, 322.0], [1609434120000, 765.07, 765.71, 764.74, 765.61, 336.0], [1609434180000, 765.8, 765.8, 764.6, 765.05, 473.0], [1609434240000, 765.17, 765.4, 764.57, 765.25, 360.0], [1609434300000, 765.12, 766.53, 765.12, 766.13, 519.0], [1609434360000, 765.91, 766.96, 765.79, 765.92, 250.0], [1609434420000, 765.99, 765.99, 765.37, 765.53, 188.0], [1609434480000, 765.92, 767.28, 765.92, 766.6, 302.0], [1609434540000, 766.95, 767.4, 765.92, 767.4, 419.0], [1609434600000, 766.74, 768.56, 766.74, 768.56, 252.0], [1609434660000, 769.09, 770.5, 768.89, 769.56, 696.0], [1609434720000, 769.64, 769.64, 768.85, 768.93, 365.0], [1609434780000, 769.08, 769.5, 769.08, 769.14, 393.0], [1609434840000, 769.07, 772.28, 768.8, 771.76, 966.0], [1609434900000, 772.39, 774.64, 772.39, 774.22, 3488.0], [1609434960000, 773.43, 773.96, 772.21, 772.21, 708.0], [1609435020000, 772.21, 774.29, 772.21, 772.97, 473.0], [1609435080000, 773.0, 773.42, 771.23, 771.61, 468.0], [1609435140000, 771.41, 772.03, 770.89, 771.01, 355.0], [1609435200000, 770.83, 770.83, 770.12, 770.71, 196.0], [1609435260000, 770.34, 772.54, 769.27, 772.54, 1081.0], [1609435320000, 772.86, 776.41, 772.86, 776.01, 1011.0], [1609435380000, 775.84, 778.77, 774.59, 778.77, 3482.0], [1609435440000, 778.62, 781.0, 777.94, 779.45, 3235.0], [1609435500000, 779.58, 780.38, 777.89, 778.28, 2401.0], [1609435560000, 777.85, 780.99, 777.57, 779.7, 891.0], [1609435620000, 779.64, 779.92, 778.85, 778.98, 316.0], [1609435680000, 779.45, 780.4, 779.37, 780.37, 944.0], [1609435740000, 779.62, 780.03, 779.37, 779.96, 416.0], [1609435800000, 779.98, 780.58, 779.49, 780.2, 1275.0], [1609435860000, 780.29, 781.1, 780.24, 780.24, 437.0], [1609435920000, 780.4, 780.74, 779.65, 779.65, 407.0], [1609435980000, 780.09, 780.18, 778.29, 778.29, 370.0], [1609436040000, 778.5, 779.96, 778.24, 778.49, 225.0], [1609436100000, 779.5, 779.5, 778.53, 778.53, 670.0], [1609436160000, 778.36, 778.72, 778.05, 778.65, 435.0], [1609436220000, 777.85, 778.15, 776.17, 777.37, 498.0], [1609436280000, 776.82, 778.32, 776.82, 778.32, 404.0], [1609436340000, 778.5, 778.77, 777.74, 778.43, 242.0]]
    i=0
    for row in t_data:
        row[0] = datetime.utcfromtimestamp(row[0]/1000).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        t_data[i] = row
        i += 1

    csv_put_contents(file='test_ohlcv.csv',data=t_data, labels=labels)

if __name__ == '__main__':
    main()
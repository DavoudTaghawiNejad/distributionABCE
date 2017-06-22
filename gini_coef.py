'''
Created on July 24, 2011
@author: Dilum Bandara
@version: 0.1
@license: Apache License v2.0

   Copyright 2012 H. M. N. Dilum Bandara, Colorado State University

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
import pandas as pd


def GRLC(values):
    '''
    Calculate Gini index, Gini coefficient, Robin Hood index, and points of
    Lorenz curve based on the instructions given in
    www.peterrosenmai.com/lorenz-curve-graphing-tool-and-gini-coefficient-calculator
    Lorenz curve values as given as lists of x & y points [[x1, x2], [y1, y2]]
    @param values: List of values
    @return: [Gini index, Gini coefficient, Robin Hood index, [Lorenz curve]]
    '''
    n = len(values)
    assert(n > 0), 'Empty list of values'
    sortedValues = sorted(values) #Sort smallest to largest

    #Find cumulative totals
    cumm = [0]
    for i in range(n):
        cumm.append(sum(sortedValues[0:(i + 1)]))

    #Calculate Lorenz points
    LorenzPoints = []
    sumYs = 0           #Some of all y values
    robinHoodIdx = -1   #Robin Hood index max(x_i, y_i)
    for i in range(1, n + 2):
        x = 100.0 * (i - 1) / n
        y = 100.0 * (cumm[i - 1] / float(cumm[n]))
        LorenzPoints.append((x, y))
        sumYs += y
        maxX_Y = x - y
        if maxX_Y > robinHoodIdx:
        	robinHoodIdx = maxX_Y

    giniIdx = 100 + (100 - 2 * sumYs)/n #Gini index

    return giniIdx


def transform_data_frame(path):
    df = pd.read_csv(path + '/household.csv')
    wage = df.pivot(index='round', columns='id', values='wage')
    profit = df.pivot(index='round', columns='id', values='profit')
    total_income = df.pivot(index='round', columns='id', values='total_income')
    capital = df.pivot(index='round', columns='id', values='capital')
    result = []
    for r in range(1, len(wage)):
          result.append({'index': r,'round': r,
                     'wage': GRLC(wage[r]),
                     'profit': GRLC(profit[r]),
                     'total_income': GRLC(total_income[r]),
                     'capital': GRLC(capital[r])})
    pd.DataFrame(result).to_csv(path + '/gini.csv')



if __name__ == '__main__':
  transform_data_frame('.')


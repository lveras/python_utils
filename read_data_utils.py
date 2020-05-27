########################################################################
############################ PDCSV #####################################

def to_pdcsv(df, path, index=False, args={}):
    if index:
        # rename index
        index_cols = list(df.index.names)
        for i in range(0, len(index_cols)):
            if pd.isna(index_cols[i]):
                index_cols[i] = f"index{i}"
            else:
                pass
        df.index.names = index_cols
        df = df.reset_index()
    else:
        pass

    dtypes = df.dtypes.to_frame().transpose().astype(str)
    dtypes[index_cols] = dtypes[index_cols] + ":index"

    return pd.concat([dtypes, df], axis=0).to_csv(path, index=False, **args)


def read_pdcsv(path, args={}):
    # Read types first line of csv
    dtypes = pd.read_csv(path, nrows=1).iloc[0]

    # set dtype and parse_dates vector from dtypes
    parse_dates = list(dtypes[dtypes.str.contains("date")].index.values)
    index_col = list(dtypes[dtypes.str.endswith(":index")].index.values)
    dtypes = dtypes.str.split(":index").str[0]

    dtype = dtypes[~dtypes.index.isin(parse_dates)].to_dict()

    # Read the rest of the lines with the types from above
    return pd.read_csv(
        path, dtype=dtype, parse_dates=parse_dates, skiprows=[1], **args
    ).set_index(index_col)


#############################################################################
###################### ANALISE EXPLORATORIA #################################

# Imprime a tabela de estatísticas
def Print_classification_report(model, X_test, y_test, prob_threshold = 0.5):
  y_pred = (model.predict_proba(X_test)[:,1] >= prob_threshold) + 0.
  print(metrics.classification_report(y_test, y_pred))
#   metrics.classification(y_test, y_pred);

  
# Plotar gráfico com a fronteira eficiente de tradeoffs precision-recall
def Classification_report_tradeoff(model, X_test, y_test, range_threshold = [0.2,0.9]):  
  range_threshold_lin = np.linspace(range_threshold[0], range_threshold[1])
  vector_precision = np.zeros(len(range_threshold_lin))
  vector_recall = np.zeros(len(range_threshold_lin))
  for i, thr in enumerate(range_threshold_lin):
    y_pred = (model.predict_proba(X_test)[:,1] >= thr) + 0.
    vector_precision[i] = metrics.precision_recall_fscore_support(y_test, y_pred)[0][1]
    vector_recall[i] =  metrics.precision_recall_fscore_support(y_test, y_pred)[1][1]
  sns.set()
  plt.plot(vector_precision, vector_recall)    
  plt.xlabel("Precision")
  plt.ylabel("Recall")
  plt.title("Tradeoff Precision-Recall Label 1");


# Plota o gráfico de features importance
def Plotar_feature_importance(model, X_test):
  fea_imp = pd.DataFrame({'imp': model.feature_importances_, 'col': X_test.columns})
  fea_imp = fea_imp.sort_values(['imp', 'col'], ascending=[True, False]).iloc[-30:]
  fea_imp.plot(kind='barh', x='col', y='imp', figsize=(10, 10), legend=None)
  plt.title('CatBoost - Feature Importance')
  plt.ylabel('Features')
  plt.xlabel('Importance')
  plt.show();

def diffdate(x,y):
    return ((x-y) / np.timedelta64(1, 'D')).astype(float)


def count_stats(serie,log = False):
    n = len(serie)
    n_missing = sum(np.isnan(serie))
    print(f"Missing values: {n_missing}/{n} ({n_missing/n*100:.1f}%)\n")
    print(f"mean value: {np.nanmean(serie)}")
    print(f"minimum value: {serie.min()}")
    print(f"quantile 25%: {np.nanpercentile(serie,25)}")
    print(f"median value: {np.nanmedian(serie)}")
    print(f"quantile 75%: {np.nanpercentile(serie,75)}")
    print(f"maximum value: {serie.max()}")
    # plt.hist(serie, bins=10);


def count_stats_cat(serie, plot = False):
    n = len(serie)
    n_missing = sum(serie.isna())
    print(f"Missing values: {n_missing}/{n} ({n_missing/n*100:.1f}%)\n")
    if plot:
        serie.value_counts()[0:10].plot(kind = "barh")
        plt.show()
    else:
        print(serie.value_counts())

    
# Finds proportion of each category in a column which has the target
def proportion_target_categorical(df, col, name_target = 'Target', plot_with = 'plotly'):
    tmp = df.groupby(col)[name_target].mean().reset_index()
    if plot_with == 'plotly':
        fig = px.bar(tmp, x = col, y = name_target, height= 300)
        fig.show();
    else:
        plt.bar(tmp[col], tmp[name_target]);


# Finds proportion of the target in a column which is numerical by agregating in bins
def proportion_target_numeric(df, col, name_target = 'Target', plot_with = 'plotly'):
    tmp = df.groupby(col)[name_target].mean().reset_index()
    if plot_with == 'plotly':
        fig = px.bar(tmp, x = col, y = name_target, height= 300)
        fig.show();
    else:
        plt.bar(tmp[col], tmp[name_target]);

import matplotlib.pyplot
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, roc_curve, recall_score, roc_auc_score, accuracy_score, precision_score, \
    classification_report, confusion_matrix

plt = matplotlib.pyplot


def find_best_threshold(model, X_value, y_value, num_steps):
    highest_f1 = 0
    best_threshold = 0
    for threshold in np.linspace(0, 1, num_steps):
        y_predict = (model.predict_proba(X_value)[:, 1] >= threshold)
        f1 = f1_score(y_value, y_predict)
        acc = accuracy_score(y_value, y_predict)
        rec = recall_score(y_value, y_predict)
        pre = precision_score(y_value, y_predict)
        if f1 > highest_f1:
            best_threshold, highest_f1, best_acc, best_rec, best_pre = \
                threshold, f1, acc, rec, pre

    return best_threshold, highest_f1, best_acc, best_rec, best_pre


class DataAnalyzeActions:

    @staticmethod
    def calculate_scores(sampling, sampling_name, x: pd.DataFrame.values, y: pd.DataFrame.values):
        sampling = sampling
        sampling_name = sampling_name
        scores = []

        best_thresh, high_f1, high_acc, high_rec, high_pre = find_best_threshold(sampling, x, y, 100)
        scores.append([sampling_name, best_thresh, high_f1, high_acc, high_rec, high_pre])

        score = pd.DataFrame(scores,
                             columns=['Sampling', 'Best Threshold', 'F1 Score', 'Accuracy', 'Recall', 'Precision'])
        return score

    def adjusted_classes(self, prob, t):
        """
        This function adjusts class predictions based on the prediction threshold (t).
        Will only work for binary classification problems.
        """
        return [1 if y >= t else 0 for y in prob]

    def precision_recall_threshold(self, y_val, fpr, tpr, thresholds, prob):
        """
        plots the precision recall curve and shows the current value for each
        by identifying the classifier's threshold (t).
        """
        # generate new class predictions based on the adjusted_classes
        # function above and view the resulting confusion matrix.
        t = 0.5
        y_pred_adj = self.adjusted_classes(prob, t)
        print(pd.DataFrame(confusion_matrix(y_val, y_pred_adj),
                           columns=['pred_neg', 'pred_pos'],
                           index=['neg', 'pos']))

        # plot the curve
        plt.figure(figsize=(8, 8))
        plt.title("Precision and Recall curve ^ = current threshold")
        plt.step(tpr, fpr, color='b', alpha=0.2,
                 where='post')
        plt.fill_between(tpr, fpr, step='post', alpha=0.2,
                         color='b')
        plt.ylim([0.05, 1.01]);
        plt.xlim([0.05, 1.01]);
        plt.xlabel('Recall');
        plt.ylabel('Precision');

        # plot the current threshold on the line
        close_default_clf = np.argmin(np.abs(thresholds - t))
        plt.plot(tpr[close_default_clf], fpr[close_default_clf], '^', c='k',
                 markersize=15)

    def precision_recall_threshold_test(self, yTest, fpr, tpr, thresholds, prob, t=0.5):
        """
        plots the precision recall curve and shows the current value for each
        by identifying the classifier's threshold (t).
        """

        # generate new class predictions based on the adjusted_classes
        # function above and view the resulting confusion matrix.
        y_pred_adj = self.adjusted_classes(prob, t)
        print(pd.DataFrame(confusion_matrix(yTest, y_pred_adj),
                           columns=['pred_neg', 'pred_pos'],
                           index=['neg', 'pos']))

        # plot the curve
        plt.figure(figsize=(8, 8))
        plt.title("Precision and Recall curve ^ = current threshold")
        plt.step(tpr, fpr, color='b', alpha=0.2,
                 where='post')
        plt.fill_between(tpr, fpr, step='post', alpha=0.2,
                         color='b')
        plt.ylim([0.05, 1.01]);
        plt.xlim([0.05, 1.01]);
        plt.xlabel('Recall');
        plt.ylabel('Precision');

        # plot the current threshold on the line
        close_default_clf = np.argmin(np.abs(thresholds - t))
        plt.plot(tpr[close_default_clf], fpr[close_default_clf], '^', c='k',
                 markersize=15)

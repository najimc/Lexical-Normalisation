#include <string.h>

#define MAX 4


int max(int n, int* list) {
  int max = list[0];
  int i;
  for (i = 1; i < n; i++) if (list[i] > max) max = list[i];
  return max;
}


int set_len(char arr[][MAX], int size, int n) {

    int count = 1, i, j, k, eq;
    for (i = 1; i < size; i++) {
      for (j = 0; j < i; j++) {
        eq = 1;
        for (k=0; k<n; k++) {
          if (arr[i][k] != arr[j][k]) { eq=0; break; }
        }
        if (eq) break;
      }
      if (i == j) count++;
    }
    return count;
}


int join_len(char arr1[][MAX], int size1, char arr2[][MAX], int size2, int n) {

  int size = size1+size2;
  char arr[size][MAX];

  int i, j;
  for (i = 0; i < size1; i++) {
    for (j = 0; j <= n; j++) {
      arr[i][j] = arr1[i][j];
    }
  }

  for (i = size1; i < size; i++) {
    for (j = 0; j <= n; j++) {
      arr[i][j] = arr2[i-size1][j];
    }
  }
  return set_len(arr, size, n);
}


int editex(char c1, char c2, int tex) {
  if (!tex)
    return (c1==c2) ? 1 : -1;
  if (c1==c2) return 2;
  char* groups[10] = {"aeiouy", "bp", "ckq", "dt", "lr", "fpv", "sxz", "csz", "mn", "gj"};
  int i;
  for (i = 0; i < 10; i++) if (strchr(groups[i], c1) && strchr(groups[i], c2)) return 1;
  return -1;
}


int needleman_wunsch(char* token1, int l1, char* token2, int l2, int tex) {

  int F[l1+1][l2+1];

  int i, j;
  for(i=0 ; i<=l1 ; i++) F[i][0] = -i;
  for(j=0 ; j<=l2 ; j++) F[0][j] = -j;

  for(i=1 ; i<=l1 ; i++) {
    for(j=1 ; j<=l2 ; j++) {
      int list[3] = {F[i-1][j] -1, F[i][j-1] -1,
        F[i-1][j-1] + editex(token1[i-1], token2[j-1], tex)};
      F[i][j] = max(3, list);
    }
  }

  return F[l1][l2];
}


int smith_waterman(char* token1, int l1, char* token2, int l2, int tex) {

  int F[l1+1][l2+1], max_score = 0;

  int i, j;
  for(i=0 ; i<=l1 ; i++) F[i][0] = 0;
  for(j=0 ; j<=l2 ; j++) F[0][j] = 0;

  for(i=1 ; i<=l1 ; i++) {
    for(j=1 ; j<=l2 ; j++) {
      int list[4] = {0, F[i-1][j] -1, F[i][j-1] -1,
        F[i-1][j-1] + editex(token1[i-1], token2[j-1], tex)};
      F[i][j] = max(4, list);
      if (F[i][j] > max_score) max_score = F[i][j];
    }
  }

  return max_score;
}


int soundex_alg(char sound[], char* token, int l) {

  char* groups[7] = {"aeiouywh", "bfpv", "cgjkqsxz", "dt", "l", "mn", "r"};

  strcpy(sound, token);

  int i, j, k;
  for (j = 0; j < 7; j++) {
    for (i = 1; i < l; i++) {
      if (strchr(groups[j], token[i])) sound[i] = j +'0';
    }
  }

  j=1, k=1;
  for (i = 1; i < l; i++) {
    if (sound[i]==sound[i-1]) continue;
    sound[j++] = sound[i];
  }
  for (i = 1; i < j; i++) if (sound[i]!='0') sound[k++] = sound[i];
  sound[k] = '\0';

  int n = MAX;
  if (k<=n) return k; else sound[n] = '\0';
  return n;
}


int soundex(char* token1, int l1, char* token2, int l2, int tex) {
  char sound1[l1]; char sound2[l2];
  int len1 = soundex_alg(sound1, token1, l1);
  int len2 = soundex_alg(sound2, token2, l2);
  return needleman_wunsch(sound1, len1, sound2, len2, tex);
}


int n_gram_alg(char gram[][MAX], char* token, int l, int n) {
  if (l<n) return 0;

  int size = l-n+1;
  int i, j, k;
  for (i = 0; i < size; i++) {
    for (k=0, j=i; j<i+n; j++) gram[i][k++] = token[j];
    gram[i][n] = '\0';
  }

  if (l==n) return 1;
  else return set_len(gram, size, n);
}


int n_gram(char* token1, int l1, char* token2, int l2, int n) {

  int size1 = l1-n+1, size2 = l2-n+1;
  char gram1[size1][MAX];
  char gram2[size2][MAX];

  int g_len1 = n_gram_alg(gram1, token1, l1, n);
  int g_len2 = n_gram_alg(gram2, token2, l2, n);

  if (g_len1==0) return g_len2;
  if (g_len2==0) return g_len1;
  int j_len = join_len(gram1, size1, gram2, size2, n);

  return 2*j_len - g_len1 - g_len2;
}

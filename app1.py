{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "e00e4eda-4bcd-4ee9-903e-73aaae8393ca",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Overwriting app.py\n"
     ]
    }
   ],
   "source": [
    "%%writefile app.py\n",
    "\n",
    "import streamlit as st\n",
    "import pandas as pd\n",
    "\n",
    "st.title(\"Nassau Candy Dashboard\")\n",
    "\n",
    "df = pd.read_csv(\"Nassau Candy Distributor.csv\")\n",
    "\n",
    "st.write(df.head())"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

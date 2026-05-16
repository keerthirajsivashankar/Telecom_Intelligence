from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, hour, dayofmonth, sum as _sum
from pyspark.sql.functions import when, lit, to_date


# --------------------------
# SESSION
# --------------------------
def create_session():
    return SparkSession.builder \
        .appName("TelecomPipeline") \
        .getOrCreate()


# --------------------------
# LOAD
# --------------------------
def load_data(spark):
    path = "data/landing/sms-call-internet-mi-2013-11-*.csv"

    df = spark.read \
        .option("header", True) \
        .option("inferSchema", True) \
        .csv(path)

    return df


# --------------------------
# CLEAN
# --------------------------
def clean_data(df):

    df = df.withColumnRenamed("CellID", "cell_id") \
           .withColumnRenamed("countrycode", "country_code")

    df = df.withColumn("datetime", to_timestamp(col("datetime")))

    usage_cols = ["smsin", "smsout", "callin", "callout", "internet"]

    for c in usage_cols:
        df = df.fillna({c: 0})

    for c in usage_cols:
        df = df.filter(col(c) >= 0)

    return df


# --------------------------
#  NEW REGION LOGIC (FIX)
# --------------------------
def assign_region(df):

    df = df.withColumn(
        "region_name",
        when(col("cell_id") < 2500, "North")
        .when(col("cell_id") < 5000, "South")
        .when(col("cell_id") < 7500, "East")
        .otherwise("West")
    )

    df = df.withColumn("city", lit("Milan"))

    return df


# --------------------------
# AGGREGATIONS
# --------------------------
def aggregate_data(df):

    df = df.withColumn("hour", hour(col("datetime")))
    df = df.withColumn("day", dayofmonth(col("datetime")))

    df = df.withColumn(
        "total_usage",
        col("smsin") + col("smsout") +
        col("callin") + col("callout") +
        col("internet")
    )

    calls_per_hour = df.groupBy("hour") \
        .agg(_sum("callin").alias("total_calls"))

    sms_per_region = df.groupBy("region_name", "day") \
        .agg(_sum("smsin").alias("total_sms"))

    internet_per_day = df.groupBy("day") \
        .agg(_sum("internet").alias("total_internet"))

    peak_hours = df.groupBy("hour") \
        .agg(_sum("total_usage").alias("usage")) \
        .orderBy(col("usage").desc()) \
        .limit(5)

    summary = df.groupBy("region_name") \
        .agg(_sum("total_usage").alias("total_usage"))

    return calls_per_hour, sms_per_region, internet_per_day, peak_hours, summary, df


# --------------------------
# WRITE
# --------------------------
def write_output(df, summary):

    df = df.withColumn("date", to_date(col("datetime")))

    df.write \
        .mode("overwrite") \
        .partitionBy("date") \
        .parquet("data/processed/usage_data")

    summary.write \
        .mode("overwrite") \
        .parquet("data/processed/summary")


# --------------------------
# MAIN PIPELINE
# --------------------------
def main():

    spark = create_session()

    df = load_data(spark)
    print(" Data loaded")

    df = clean_data(df)
    print(" Data cleaned")

    # column pruning
    df = df.select(
        "cell_id",
        "datetime",
        "smsin",
        "smsout",
        "callin",
        "callout",
        "internet"
    )

    # performance
    df = df.repartition("cell_id")
    df = df.cache()
    df.count()

    #  FIXED HERE
    df = assign_region(df)
    print(" Region assigned")

    # DEBUG CHECK (IMPORTANT)
    df.select("cell_id", "region_name").show(10)

    print("------ Execution Plan ------")
    df.explain()

    calls_per_hour, sms_per_region, internet_per_day, peak_hours, summary, df = aggregate_data(df)

    write_output(df, summary)

    print("Data written to Parquet")

    spark.stop()


if __name__ == "__main__":
    main()

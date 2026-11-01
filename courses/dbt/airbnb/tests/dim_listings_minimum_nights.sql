-- Singular test: a plain SELECT that returns the BAD rows.
-- dbt runs this query during `dbt test`:
--   0 rows returned  -> test PASSES
--   1+ rows returned -> test FAILS (and the rows go to the _test_failures schema,
--                       because dbt_project.yml sets store_failures: true)

SELECT
    *                                        -- return the whole bad row, so you can see what is wrong
FROM
    {{ ref('dim_listings_cleansed') }}       -- ref() also tells dbt this test depends on this model
WHERE
    minimum_nights < 1                       -- the rule: after cleansing, every listing needs at least 1 night
LIMIT 10                                     -- we only need a few examples, not all bad rows

-- Custom GENERIC test: works like unique/not_null — you attach it to any column in a .yml file.
-- dbt fills in the two arguments for you:
--   model       -> the model the test is attached to
--   column_name -> the column the test is attached to
-- Like every test: return the BAD rows, 0 rows = PASS.

{% test positive_value(model, column_name) %}    {# `test` instead of `macro` makes it a generic test #}
    SELECT
        *                                        -- the whole bad row
    FROM
        {{ model }}                              -- e.g. AIRBNB.DEV.DIM_LISTINGS_CLEANSED
    WHERE
        {{ column_name }} < 1                    -- e.g. minimum_nights < 1  -> bad
{% endtest %}

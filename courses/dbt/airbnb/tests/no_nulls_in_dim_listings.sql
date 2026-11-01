-- Singular test that just calls our macro.
-- The macro writes the whole SELECT for us: any row with a NULL in ANY column fails the test.
{{ no_nulls_in_columns(ref('dim_listings_cleansed')) }}

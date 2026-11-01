-- Singular test: a review can't be written before its listing existed.
-- Returns the BAD rows: reviews dated earlier than the listing's created_at.
-- 0 rows -> PASS.

SELECT
    r.listing_id,                              -- which listing
    r.review_date,                             -- when the review was written
    l.created_at                               -- when the listing was created
FROM
    {{ ref('fct_reviews') }} r                 -- every review (fact table)
JOIN
    {{ ref('dim_listings_cleansed') }} l       -- the listing each review belongs to
    ON r.listing_id = l.listing_id             -- match review -> listing
WHERE
    r.review_date < l.created_at               -- the rule is broken if the review is older than the listing
LIMIT 10                                       -- a few examples are enough to debug

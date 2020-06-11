CREATE DATABASE dockerproject;
use dockerproject;

CREATE TABLE variants (
    chromosome CHAR(100),
    position CHAR(100),
    reference CHAR(100),
    alternative CHAR(100),
    total_alleles CHAR(100),
    allele_frequency CHAR(100),
    variant_type CHAR(100),
    allele_type CHAR(100),
    non_cancer_total_alleles CHAR(100)

);


CREATE USER 'root'@'%' IDENTIFIED BY 'root'

grant all on *.* to 'root'@'%';

-- CREATE DATABASE knights;
-- use knights;
--
-- CREATE TABLE favorite_colors (
--   name VARCHAR(20),
--   color VARCHAR(10)
-- );
--
-- INSERT INTO favorite_colors
--   (name, color)
-- VALUES
--   ('Lancelot', 'blue'),
--   ('Galahad', 'yellow');

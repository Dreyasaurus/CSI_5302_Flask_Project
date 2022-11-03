ALTER TABLE Batting
    CHANGE COLUMN `2b`   -- old name; notice optional backticks
                   b2        -- new name
                   smallint(6);
				   
ALTER TABLE Batting
    CHANGE COLUMN `3B`   -- old name; notice optional backticks
                   b3        -- new name
                   smallint(6);
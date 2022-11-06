DELIMITER //

CREATE OR REPLACE PROCEDURE carrer_summary (
IN pPlayerId varchar(9)
)
 BEGIN
  SELECT SUM(h) as sumHits, SUM(AB) as sumAB,SUM(hr) as sumHr, IFNULL(SUM(h)/ SUM(AB),0) as ba, SUM(R) as sumR, SUM(RBI) as SumRBI, SUM(sb) as sumSB
  from BATTING WHERE playerId = pPlayerId GROUP BY playerId;
 END;
//

DELIMITER ;
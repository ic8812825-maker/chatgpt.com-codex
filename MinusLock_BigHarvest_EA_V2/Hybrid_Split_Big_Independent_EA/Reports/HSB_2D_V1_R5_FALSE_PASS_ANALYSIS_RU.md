# R5 false-PASS analysis

R4 удалял все `return HSBI_RuntimeReject(...)` regex-правилом без классификации status expression. Поэтому enum cast zero и alias могли создать valid status, а вычисляемая запись `r.valid=...` не нарушала слабый constructor proof. R5 создаёт return nodes, разрешает ранний reject только для точного allowlisted identifier, нормализует reversed equality/inequality и требует strict-whitelist constructor без любых valid writes и вторичных status/reason writes.

M136 одновременно внедряет computed valid и reversed enum-zero bypass; ожидаются S028 и SREJECT при S045 PASS.

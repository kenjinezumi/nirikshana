CREATE TRIGGER 'ISO_metadata_reference_row_id_value_update'
BEFORE UPDATE OF 'row_id_value' ON 'ISO_metadata_reference'
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'update on table ISO_metadata_reference violates constraint: row_id_value must be 0 when reference_scope is ''table'' or ''column''')
WHERE NEW.reference_scope IN ('table','column') AND NEW.row_id_value <> 0;
SELECT RAISE(ROLLBACK, 'update on ISO_table metadata_reference violates constraint: row_id_value must exist in specified table when reference_scope is ''row'' or ''row/col''')
WHERE NEW.reference_scope IN ('row','row/col') AND NOT EXISTS
(SELECT eval('SELECT rowid FROM ' || NEW.table_name ||
' WHERE rowid = ' || NEW.row_id_value));
END;


CREATE TRIGGER 'ISO_metadata_reference_row_id_value_insert'
BEFORE INSERT ON 'ISO_metadata_reference'
FOR EACH ROW BEGIN
SELECT RAISE(ROLLBACK, 'insert on ISO_table ISO_metadata_reference violates constraint: row_id_value must be 0 when reference_scope is ''table'' or ''column''')
WHERE NEW.reference_scope IN ('table','column') AND NEW.row_id_value <> 0;
SELECT RAISE(ROLLBACK, 'insert on table ISO_metadata_reference violates constraint: row_id_value must exist in specified table when reference_scope is ''row'' or ''row/col''')
WHERE NEW.reference_scope IN ('row','row/col') AND NOT EXISTS
(SELECT eval('SELECT rowid FROM ' || NEW.table_name ||
' WHERE rowid = ' || NEW.row_id_value));
END;

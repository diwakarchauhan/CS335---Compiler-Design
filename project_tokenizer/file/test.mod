IMPLEMENTATION MODULE ShapeMod;
   TYPE
      Shape = POINTER TO RECORD
         disposeThis: PROCEDURE (VAR Shape);
         draw: PROCEDURE (Shape);
         moveTo: PROCEDURE (Shape, INTEGER, INTEGER);
         rMoveTo: PROCEDURE (Shape, INTEGER, INTEGER);
      END;

      (*
         *** Note:  The fields from the Shape structure must be placed first
             in any subclass structure. If this Shape structure is redefined,
             the structure must also be redefined in the subclasses to
             maintain the one-to-one correspondance in the lead in fields.
      *)
END ShapeMod.

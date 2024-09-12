var dagAPIFuncs = (window.dashAgGridAPIFunctions =
  window.dashAgGridAPIFunctions || {});

// dagAPIFuncs.startEditingNewRow = function (row_id, id) {
dagAPIFuncs.startEditingNewRow = (row_id, id) => {
  if (row_id) {
    console.log("row_id = " + row_id);
    // Access the grid API asynchronously after the row data is updated
    dash_ag_grid.getApiAsync(id).then((grid) => {
      // Listen for the 'rowDataUpdated' event to ensure the row is fully added
      grid.addEventListener("rowDataUpdated", () => {
        const rowNode = grid.getRowNode(row_id); // Directly get the row node by its ID

        if (rowNode) {
          // Find the first editable column dynamically
          const editableColumn = grid
            .getColumnDefs()
            .find((colDef) => colDef.editable);

          if (editableColumn) {
            // Start editing the new row's first editable column
            grid.startEditingCell({
              rowIndex: rowNode.rowIndex,
              colKey: editableColumn.field, // Use the field name of the first editable column
            });
          }
        }
      });
    });
  }
  return null;
};

dagAPIFuncs.stopEditing = (row_id, id) => {
  if (row_id) {
    console.log("row_id = " + row_id);
    // Access the grid API asynchronously after the row data is updated
    dash_ag_grid.getApiAsync(id).then((grid) => {
      grid.stopEditing();
    });
  }
  return null;
};

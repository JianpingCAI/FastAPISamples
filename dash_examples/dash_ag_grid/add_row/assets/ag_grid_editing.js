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
          // Start editing the new row's 'name' field
          grid.startEditingCell({
            rowIndex: rowNode.rowIndex,
            colKey: "name",
          });
        }
      });
    });
  }
  return null;
};

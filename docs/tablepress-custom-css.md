# TablePress Custom CSS Backup

This file backs up the TablePress custom CSS applied via WordPress Customizer → Additional CSS.
Keep this in sync if the live site styling changes.

## Purpose

- Hide the TablePress "Edit" link from public frontend.
- Apply DigiTrust Lab brand colors to TablePress tables.
- Improve cell padding and row readability.

## CSS Snippet

```css
/* Hide TablePress edit link from frontend */
.tablepress caption { display: none !important; }

/* TablePress brand styling */
.tablepress thead th,
.tablepress tfoot th {
  background-color: #E8621A !important;
  color: #FFFFFF !important;
  font-weight: 600 !important;
  border: none !important;
}
.tablepress thead th,
.tablepress tfoot th,
.tablepress tbody td {
  padding: 14px 16px !important;
  border-color: #EBEBEB !important;
}
.tablepress tbody tr:nth-child(even) {
  background-color: #F5F3EE !important;
}
.tablepress tbody tr:nth-child(odd) {
  background-color: #FFFFFF !important;
}
.tablepress tbody tr:hover {
  background-color: #FAF5F0 !important;
}
.tablepress .row-hover tr:hover td {
  background-color: #FAF5F0 !important;
}
```

## Where it lives

- **Primary location:** WordPress Customizer → Additional CSS
- **Backup:** This file

## Important note

TablePress tables should always be inserted into posts using the `[table id=N /]` shortcode, **not** hardcoded HTML, so that live edits in the TablePress admin propagate correctly.

Last updated: 2026-07-26

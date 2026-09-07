# Expected native surveydown export fixture for greedyQ 0.1.0-draft.1.
# This file is independently authored and has not yet been generated or executed.

library(surveydown)

db <- sd_db_connect()
ui <- sd_ui()

server <- function(input, output, session) {
  # A conforming exporter will generate deterministic equivalents for:
  # - consent/refusal routing
  # - age screening
  # - persisted two-arm assignment
  # - condition-page routing
  # - conditional follow-up questions
  # - completion and withdrawal outcomes
  #
  # Exact generated calls remain blocked on the v0.1 exporter implementation.
  # See compatibility-report.json; this fixture must not be described as runnable.

  sd_server(db = db)
}

shiny::shinyApp(ui = ui, server = server)

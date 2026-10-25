# Generated independently by greedyQ 0.2.
# Review and test this native surveydown export before fielding.
library(shiny)
library(surveydown)

db <- sd_db_connect()
ui <- sd_ui()
server <- function(input, output, session) {
  sd_show_if(
    (sd_value("primary_use") == "other") ~ "primary_use_other",
    (sd_value("overall_satisfaction") <= 3) ~ "low_satisfaction_reason",
    (sd_value("had_problem") == "yes") ~ "problem_area",
    (sd_value("had_problem") == "yes") ~ "problem_detail",
    (sd_value("withdraw_now") == "withdraw") ~ "deletion_request"
  )
  sd_skip_if(
    (sd_value("consent_choice") == "no") ~ "consent_refused",
    (sd_value("age") < 18) ~ "screened_out",
    (sd_value("withdraw_now") == "withdraw") ~ "withdrawn",
    (sd_value("used_greedyq") == "no") ~ "screened_out",
    (sd_value("withdraw_now") == "submit") ~ "complete"
  )
  sd_stop_if(
    (sd_value("age") > 120) ~ "Enter an age of 120 or less.",
    ((sd_value("recommend_score") < 0) | (sd_value("recommend_score") > 10)) ~ "Enter a number from 0 to 10.",
    ((sd_value("had_problem") == "yes") & !sd_is_answered("problem_area")) ~ "Choose the area where the most important problem occurred.",
    ((sd_value("withdraw_now") == "withdraw") & !sd_is_answered("deletion_request")) ~ "Confirm that withdrawing deletes this session's answers before continuing."
  )
  sd_server(db = db)
}
shiny::shinyApp(ui = ui, server = server)

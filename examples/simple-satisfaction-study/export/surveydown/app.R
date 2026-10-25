# Generated independently by greedyQ 0.2.
# Review and test this native surveydown export before fielding.
library(shiny)
library(surveydown)

db <- sd_db_connect()
ui <- sd_ui()
server <- function(input, output, session) {
  gq_collection <- function(value) {
    if (is.null(value)) return(character())
    value <- value[!is.na(value)]
    value <- value[nzchar(as.character(value))]
    unlist(strsplit(as.character(value), "|", fixed = TRUE), use.names = FALSE)
  }
  sd_show_if(
    isTRUE(!is.null(sd_value("primary_use")) && (sd_value("primary_use") == "other")) ~ "primary_use_other",
    isTRUE(!is.null(sd_value("overall_satisfaction")) && (sd_value("overall_satisfaction") <= 3)) ~ "low_satisfaction_reason",
    isTRUE(!is.null(sd_value("had_problem")) && (sd_value("had_problem") == "yes")) ~ "problem_area",
    isTRUE(!is.null(sd_value("had_problem")) && (sd_value("had_problem") == "yes")) ~ "problem_detail",
    isTRUE(!is.null(sd_value("withdraw_now")) && (sd_value("withdraw_now") == "withdraw")) ~ "deletion_request"
  )
  sd_skip_if(
    isTRUE(!is.null(sd_value("consent_choice")) && (sd_value("consent_choice") == "no")) ~ "consent_refused",
    isTRUE(!is.null(sd_value("age")) && (sd_value("age") < 18)) ~ "screened_out",
    isTRUE(!is.null(sd_value("withdraw_now")) && (sd_value("withdraw_now") == "withdraw")) ~ "withdrawn",
    isTRUE(!is.null(sd_value("used_greedyq")) && (sd_value("used_greedyq") == "no")) ~ "screened_out",
    isTRUE(!is.null(sd_value("withdraw_now")) && (sd_value("withdraw_now") == "submit")) ~ "complete"
  )
  sd_stop_if(
    isTRUE(!is.null(sd_value("age")) && (sd_value("age") > 120)) ~ "Enter an age of 120 or less.",
    (isTRUE(!is.null(sd_value("recommend_score")) && (sd_value("recommend_score") < 0)) | isTRUE(!is.null(sd_value("recommend_score")) && (sd_value("recommend_score") > 10))) ~ "Enter a number from 0 to 10.",
    (isTRUE(!is.null(sd_value("had_problem")) && (sd_value("had_problem") == "yes")) & !sd_is_answered("problem_area")) ~ "Choose the area where the most important problem occurred.",
    (isTRUE(!is.null(sd_value("withdraw_now")) && (sd_value("withdraw_now") == "withdraw")) & !sd_is_answered("deletion_request")) ~ "Confirm that withdrawing deletes this session's answers before continuing."
  )
  sd_server(db = db)
}
shiny::shinyApp(ui = ui, server = server)

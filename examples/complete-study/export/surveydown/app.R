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
  assignment_condition <- sample(c("control", "treatment"), 1, prob = c(1, 1))
  sd_store_value(assignment_condition)
  sd_show_if(
    isTRUE((assignment_condition == "control")) ~ "stimulus_control",
    isTRUE((assignment_condition == "treatment")) ~ "stimulus_treatment",
    isTRUE(!is.null(sd_value("support_post")) && (sd_value("support_post") <= 3)) ~ "opposition_reason",
    isTRUE(!is.null(sd_value("gender")) && (sd_value("gender") == "self_describe")) ~ "gender_self_description",
    isTRUE(!is.null(sd_value("withdraw_now")) && (sd_value("withdraw_now") == "withdraw")) ~ "deletion_request"
  )
  sd_skip_if(
    isTRUE(!is.null(sd_value("consent_choice")) && (sd_value("consent_choice") == "no")) ~ "consent_refused",
    isTRUE(!is.null(sd_value("age")) && (sd_value("age") < 18)) ~ "screened_out",
    isTRUE(!is.null(sd_value("withdraw_now")) && (sd_value("withdraw_now") == "withdraw")) ~ "withdrawn",
    isTRUE(!is.null(sd_value("withdraw_now")) && (sd_value("withdraw_now") == "submit")) ~ "complete"
  )
  sd_stop_if(
    isTRUE(!is.null(sd_value("age")) && (sd_value("age") > 120)) ~ "Enter an age of 120 or less.",
    !sd_is_answered("attention_check") ~ "Select one response. The requested answer is Somewhat agree.",
    (isTRUE(!is.null(sd_value("withdraw_now")) && (sd_value("withdraw_now") == "withdraw")) & !sd_is_answered("deletion_request")) ~ "Confirm that withdrawing deletes this session's answers before continuing."
  )
  sd_server(db = db)
}
shiny::shinyApp(ui = ui, server = server)

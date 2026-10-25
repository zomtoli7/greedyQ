# Generated independently by greedyQ 0.2.
# Review and test this native surveydown export before fielding.
library(shiny)
library(surveydown)

db <- sd_db_connect()
ui <- sd_ui()
server <- function(input, output, session) {
  assignment_condition <- sample(c("control", "treatment"), 1, prob = c(1, 1))
  sd_store_value(assignment_condition)
  sd_show_if(
    (assignment_condition == "control") ~ "stimulus_control",
    (assignment_condition == "treatment") ~ "stimulus_treatment",
    (sd_value("support_post") <= 3) ~ "opposition_reason",
    (sd_value("gender") == "self_describe") ~ "gender_self_description",
    (sd_value("withdraw_now") == "withdraw") ~ "deletion_request"
  )
  sd_skip_if(
    (sd_value("consent_choice") == "no") ~ "consent_refused",
    (sd_value("age") < 18) ~ "screened_out",
    (sd_value("withdraw_now") == "withdraw") ~ "withdrawn",
    (sd_value("withdraw_now") == "submit") ~ "complete"
  )
  sd_stop_if(
    (sd_value("age") > 120) ~ "Enter an age of 120 or less.",
    !sd_is_answered("attention_check") ~ "Select one response. The requested answer is Somewhat agree.",
    ((sd_value("withdraw_now") == "withdraw") & !sd_is_answered("deletion_request")) ~ "Confirm that withdrawing deletes this session's answers before continuing."
  )
  sd_server(db = db)
}
shiny::shinyApp(ui = ui, server = server)

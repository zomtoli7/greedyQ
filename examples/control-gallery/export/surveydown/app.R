# Generated independently by greedyQ 0.2.
# Review and test this native surveydown export before fielding.
library(shiny)
library(surveydown)

db <- sd_db_connect()
ui <- sd_ui()
server <- function(input, output, session) {
  sd_show_if(
    (sd_value("conditional_choice") == "yes") ~ "conditional_text"
  )
  output$gq_audio_example_output <- renderUI({ tags$audio(src = "https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3", controls = NA, style = 'max-width:100%;') })
  gq_audio_example_value <- reactive(NULL)
  sd_question_custom(
    id = "audio_example",
    label = "Audio stimulus (greedyQ extension)",
    output = uiOutput("gq_audio_example_output"),
    value = gq_audio_example_value
  )
  output$gq_video_example_output <- renderUI({ tags$video(src = "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4", controls = NA, style = 'max-width:100%;') })
  gq_video_example_value <- reactive(NULL)
  sd_question_custom(
    id = "video_example",
    label = "Video stimulus (greedyQ extension)",
    output = uiOutput("gq_video_example_output"),
    value = gq_video_example_value
  )
  output$gq_rank_example_output <- renderUI({ tagList(selectInput("rank_example_ease", "Ease of use", choices = 1:3), selectInput("rank_example_speed", "Speed", choices = 1:3), selectInput("rank_example_flexibility", "Flexibility", choices = 1:3)) })
  gq_rank_example_value <- reactive(list("ease" = input$rank_example_ease, "speed" = input$rank_example_speed, "flexibility" = input$rank_example_flexibility))
  sd_question_custom(
    id = "rank_example",
    label = "Rank these priorities",
    output = uiOutput("gq_rank_example_output"),
    value = gq_rank_example_value
  )
  output$gq_sbs_example_output <- renderUI({ tagList(selectInput("sbs_example_current_clear", "Current — Clear", choices = c("Low" = 1, "Medium" = 2, "High" = 3)), selectInput("sbs_example_current_useful", "Current — Useful", choices = c("Low" = 1, "Medium" = 2, "High" = 3)), selectInput("sbs_example_proposed_clear", "Proposed — Clear", choices = c("Low" = 1, "Medium" = 2, "High" = 3)), selectInput("sbs_example_proposed_useful", "Proposed — Useful", choices = c("Low" = 1, "Medium" = 2, "High" = 3))) })
  gq_sbs_example_value <- reactive(list("current.clear" = input$sbs_example_current_clear, "current.useful" = input$sbs_example_current_useful, "proposed.clear" = input$sbs_example_proposed_clear, "proposed.useful" = input$sbs_example_proposed_useful))
  sd_question_custom(
    id = "sbs_example",
    label = "Rate both versions",
    output = uiOutput("gq_sbs_example_output"),
    value = gq_sbs_example_value
  )
  output$gq_nps_example_output <- renderUI({ radioButtons("nps_example", NULL, choices = c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), inline = TRUE) })
  gq_nps_example_value <- reactive(input$nps_example)
  sd_question_custom(
    id = "nps_example",
    label = "How likely are you to recommend greedyQ?",
    output = uiOutput("gq_nps_example_output"),
    value = gq_nps_example_value
  )
  output$gq_timing_example_output <- renderUI({ tags$span('Timing is recorded by the generated server binding.') })
  gq_timing_example_value <- local({ started <- Sys.time(); reactive({ invalidateLater(1000); as.numeric(difftime(Sys.time(), started, units = 'secs')) }) })
  sd_question_custom(
    id = "timing_example",
    label = "Time on this page",
    output = uiOutput("gq_timing_example_output"),
    value = gq_timing_example_value
  )
  output$gq_sum_example_output <- renderUI({ tagList(numericInput("sum_example_design", "Design", value = 0, min = 0), numericInput("sum_example_testing", "Testing", value = 0, min = 0), numericInput("sum_example_documentation", "Documentation", value = 0, min = 0)) })
  gq_sum_example_value <- reactive(list("design" = input$sum_example_design, "testing" = input$sum_example_testing, "documentation" = input$sum_example_documentation))
  sd_question_custom(
    id = "sum_example",
    label = "Allocate 100 points",
    output = uiOutput("gq_sum_example_output"),
    value = gq_sum_example_value
  )
  output$gq_group_rank_example_output <- renderUI({ tagList(selectInput("group_rank_example_speed_group", "Speed — group", choices = c("Essential" = "essential", "Optional" = "optional")), numericInput("group_rank_example_speed_rank", "Speed — rank", value = 1, min = 1), selectInput("group_rank_example_trust_group", "Trust — group", choices = c("Essential" = "essential", "Optional" = "optional")), numericInput("group_rank_example_trust_rank", "Trust — rank", value = 1, min = 1), selectInput("group_rank_example_ease_group", "Ease — group", choices = c("Essential" = "essential", "Optional" = "optional")), numericInput("group_rank_example_ease_rank", "Ease — rank", value = 1, min = 1)) })
  gq_group_rank_example_value <- reactive(list("speed" = reactiveValuesToList(input)[c("group_rank_example_speed_group", "group_rank_example_speed_rank")], "trust" = reactiveValuesToList(input)[c("group_rank_example_trust_group", "group_rank_example_trust_rank")], "ease" = reactiveValuesToList(input)[c("group_rank_example_ease_group", "group_rank_example_ease_rank")]))
  sd_question_custom(
    id = "group_rank_example",
    label = "Group and rank these items",
    output = uiOutput("gq_group_rank_example_output"),
    value = gq_group_rank_example_value
  )
  output$gq_drill_example_output <- renderUI({ selectInput("drill_example", NULL, choices = c("Asia > Korea > Seoul" = "kr_seoul", "Asia > Korea > Busan" = "kr_busan", "Europe > France > Paris" = "fr_paris")) })
  gq_drill_example_value <- reactive(input$drill_example)
  sd_question_custom(
    id = "drill_example",
    label = "Choose a location",
    output = uiOutput("gq_drill_example_output"),
    value = gq_drill_example_value
  )
  output$gq_custom_example_output <- renderUI({ selectInput("custom_example", NULL, choices = c("First" = "first", "Second" = "second")) })
  gq_custom_example_value <- reactive(input$custom_example)
  sd_question_custom(
    id = "custom_example",
    label = "Custom control based on a built-in template",
    output = uiOutput("gq_custom_example_output"),
    value = gq_custom_example_value
  )
  sd_server(db = db)
}
shiny::shinyApp(ui = ui, server = server)

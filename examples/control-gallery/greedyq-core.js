/* greedyQ browser core v0.2.0-draft.1. Copy byte-for-byte; do not customize. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.greedyQ = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  const VERSION = "0.2.0-draft.1";
  const RELEASE = "0.2_2026-10-25_7beafe4";
  // Generated from greedyq/locale-messages.json; parity is tested.
  const LOCALE_MESSAGES = {"Survey link incomplete":["설문 링크를 확인해 주세요","请检查问卷链接","請檢查問卷連結"],"Please return to Prolific and open the study from your task page.":["Prolific으로 돌아가 과제 페이지에서 연구를 열어 주세요.","请返回 Prolific，从任务页面打开本研究。","請返回 Prolific，從任務頁面開啟本研究。"],"Survey unavailable":["설문을 열 수 없습니다","无法打开问卷","無法開啟問卷"],"The secure data connection could not be started.":["안전한 데이터 연결을 시작하지 못했습니다.","无法建立安全的数据连接。","無法建立安全的資料連線。"],"Your response could not be saved. Please check your connection before continuing.":["응답을 저장하지 못했습니다. 연결을 확인한 뒤 계속해 주세요.","无法保存您的回答，请检查网络连接后继续。","無法儲存您的回答，請檢查網路連線後繼續。"],"Choose one":["하나를 선택하세요","请选择一项","請選擇一項"],"Transcript":["대본","文字稿","文字稿"],"Research team":["연구팀","研究团队","研究團隊"],"greedyQ Survey":["greedyQ 설문","greedyQ 问卷","greedyQ 問卷"],"Option":["선택지","选项","選項"],"Your browser does not support audio playback.":["이 브라우저는 오디오 재생을 지원하지 않습니다.","您的浏览器不支持音频播放。","您的瀏覽器不支援音訊播放。"],"Your browser does not support video playback.":["이 브라우저는 비디오 재생을 지원하지 않습니다.","您的浏览器不支持视频播放。","您的瀏覽器不支援影片播放。"],"Previous":["이전","上一页","上一頁"],"Continue":["계속하기","继续","繼續"],"Please answer the required questions before continuing.":["필수 문항에 응답해 주세요.","请回答必答题后继续。","請回答必答題後繼續。"],"Select all that apply.":["해당되는 모든 것을 선택하세요.","请选择所有适用的选项。","請選擇所有適用的選項。"],"Complete":["종료","已结束","已結束"],"completed":["응답 완료","作答完成","作答完成"],"screened_out":["참여 대상이 아닙니다","不符合参与条件","不符合參與條件"],"consent_declined":["참여하지 않음","未同意参与","未同意參與"],"consent_refused":["참여하지 않음","未同意参与","未同意參與"],"technical_error":["설문을 계속할 수 없습니다","无法继续问卷","無法繼續問卷"],"withdrawn":["참여 철회","已退出参与","已退出參與"],"Rank":["순위","排序","排序"],"Choose":["선택하세요","请选择","請選擇"],"Group":["그룹","分组","分組"],"Level":["단계","层级","層級"],"Start":["시작일","开始日期","開始日期"],"End":["종료일","结束日期","結束日期"],"s":["초","秒","秒"],"minimum":["최솟값","最小值","最小值"],"maximum":["최댓값","最大值","最大值"],"required":["필수","必答","必答"],"Not at all likely":["전혀 의향 없음","完全不可能","完全不可能"],"Extremely likely":["매우 의향 있음","非常可能","非常可能"],"Use each rank only once.":["각 순위는 한 번만 사용하세요.","每个名次只能使用一次。","每個名次只能使用一次。"],"Rank every item.":["모든 항목의 순위를 정해 주세요.","请为所有项目排序。","請為所有項目排序。"],"The allocation must total {total}.":["합계가 {total}이 되도록 입력해 주세요.","分配总和必须为 {total}。","分配總和必須為 {total}。"],"Answer every row in every column.":["모든 열의 각 행에 응답하세요.","请回答每一列中的每一行。","請回答每一欄中的每一列。"],"Place every item in a group.":["모든 항목을 그룹에 배치하세요.","请将每个项目放入一个组。","請將每個項目放入一個組。"],"Use each rank only once within {group}.":["{group} 내에서 각 순위를 한 번만 사용하세요.","在 {group} 中，每个名次只能使用一次。","在 {group} 中，每個名次只能使用一次。"],"Complete every level of the selection.":["모든 단계에서 선택해 주세요.","请完成所有层级的选择。","請完成所有層級的選擇。"],"Please enter a value within the allowed range and format.":["허용된 범위와 형식에 맞게 입력해 주세요.","请按允许的范围和格式输入。","請按允許的範圍和格式輸入。"],"Route error":["설문 경로 오류","问卷路径错误","問卷路徑錯誤"],"The next page is unavailable.":["다음 페이지를 열 수 없습니다.","无法打开下一页。","無法開啟下一頁。"],"Your response could not be saved. Please try again.":["응답을 저장하지 못했습니다. 다시 시도해 주세요.","无法保存您的回答，请重试。","無法儲存您的回答，請重試。"],"Response not saved. Please retry before leaving.":["응답이 저장되지 않았습니다. 나가기 전에 다시 시도하세요.","回答尚未保存，请在离开前重试。","回答尚未儲存，請在離開前重試。"],"Please confirm consent before random assignment.":["무작위 배정 전에 참여 동의를 확인해 주세요.","随机分配前请确认参与同意。","隨機分配前請確認參與同意。"],"Random assignment could not be completed. Please try again.":["무작위 배정을 완료하지 못했습니다. 다시 시도해 주세요.","无法完成随机分配，请重试。","無法完成隨機分配，請重試。"],"Participation withdrawn":["참여를 철회했습니다","已退出参与","已退出參與"],"(Timer running in the background; nothing is shown to participants.)":["(백그라운드에서 타이머가 돌아가고 있음, 실제 화면엔 아무것도 나타나지 않음)","（计时器正在后台运行，参与者不会看到任何内容。）","（計時器正在背景執行，參與者不會看到任何內容。）"],"Continue to the next website":["다음 웹사이트로 이동","前往下一个网站","前往下一個網站"],"Return":["돌아가기","返回","返回"],"Completion code":["완료 코드","完成代码","完成代碼"],"A response already exists. Reopen this study in the browser where you started, or contact the researcher.":["이미 참여 기록이 있습니다. 처음 참여한 브라우저에서 연구를 다시 열거나 연구자에게 문의해 주세요.","已有参与记录。请在最初参与的浏览器中重新打开研究，或联系研究者。","已有參與紀錄。請在最初參與的瀏覽器中重新開啟研究，或聯絡研究者。"],"Return link unavailable.":["반환 링크를 사용할 수 없습니다.","返回链接不可用。","返回連結無法使用。"]," (preview: no external navigation)":[" (미리보기: 외부 이동 안 함)","（预览：不会跳转到外部页面）","（預覽：不會跳轉至外部頁面）"],"Please review this answer.":["이 응답을 확인해 주세요.","请检查此回答。","請檢查此回答。"],"Survey closed":["설문이 종료되었습니다","问卷已关闭","問卷已關閉"],"This study is no longer accepting responses. Please contact the research team if you need help.":["이 연구는 더 이상 응답을 받지 않습니다. 도움이 필요하면 연구팀에 연락해 주세요.","本研究已停止接收回答。如需帮助，请联系研究团队。","本研究已停止接收回答。如需協助，請聯絡研究團隊。"],"Move the slider to answer.":["슬라이더를 움직여 응답해 주세요.","请移动滑块作答。","請移動滑桿作答。"],"Local preview only. Answers stay in this browser and are not sent to the researcher.":["로컬 미리보기입니다. 응답은 이 브라우저에만 남으며 연구자에게 전달되지 않습니다.","仅供本地预览。回答只保存在此浏览器，不会发送给研究者。","僅供本地預覽。回答只保存在此瀏覽器，不會傳送給研究者。"]};
  const LANGUAGES = ['en','ko','zh-CN','zh-TW'];
  function translate(language, message, values={}) {
    if(!LANGUAGES.includes(language))throw new Error('Choose en, ko, zh-CN or zh-TW for greedyq.language.');
    const template=language==='en'?message:(LOCALE_MESSAGES[message]?.[LANGUAGES.indexOf(language)-1] ?? message);
    return template.replace(/\{(\w+)\}/g,(match,key)=>Object.hasOwn(values,key)?String(values[key]):match);
  }
  const PAGE_RE = /^---\s+([A-Za-z][A-Za-z0-9_-]*)\s*$/gm;
  const FENCE_RE = /```\{r\}\s*\n([\s\S]*?)```/g;
  const CALL_RE = /\b(sd_question|sd_nav)\s*\(/;
  const TYPES = new Set([
    "text",
    "textarea",
    "numeric",
    "mc",
    "mc_multiple",
    "mc_buttons",
    "mc_multiple_buttons",
    "mc_image",
    "mc_multiple_image",
    "select",
    "slider",
    "slider_numeric",
    "date",
    "daterange",
    "matrix",
    "matrix_multiple",
    "audio",
    "video",
    "rank_order",
    "side_by_side",
    "nps",
    "timing",
    "constant_sum",
    "pick_group_rank",
    "drill_down",
    "custom",
  ]);
  const ID_RE = /^[a-z][a-z0-9_]{1,63}$/;

  class ParseError extends Error {
    constructor(message, line) {
      super((line ? `Line ${line}: ` : "") + message);
      this.name = "ParseError";
      this.line = line || null;
    }
  }
  function scalar(raw) {
    const value = String(raw).trim();
    if (
      (value[0] === '"' && value.at(-1) === '"') ||
      (value[0] === "'" && value.at(-1) === "'")
    )
      return value
        .slice(1, -1)
        .replace(/\\n/g, "\n")
        .replace(/\\"/g, '"')
        .replace(/\\\\/g, "\\");
    if (/^(true|TRUE|True)$/.test(value)) return true;
    if (/^(false|FALSE|False)$/.test(value)) return false;
    if (/^(null|NULL|~)$/.test(value)) return null;
    if (/^-?\d+$/.test(value)) return Number.parseInt(value, 10);
    if (/^-?(?:\d+\.\d*|\d*\.\d+)$/.test(value))
      return Number.parseFloat(value);
    if (value.startsWith("[") && value.endsWith("]"))
      return splitTop(value.slice(1, -1)).map(scalar);
    if (value.startsWith("{") && value.endsWith("}"))
      return Object.fromEntries(
        splitTop(value.slice(1, -1)).map((x) => {
          const p = splitKey(x);
          return [p[0], scalar(p[1])];
        }),
      );
    return value;
  }
  function stripComment(line) {
    let quote = null,
      escaped = false;
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (quote) {
        if (escaped) escaped = false;
        else if (c === "\\" && quote === '"') escaped = true;
        else if (c === quote) quote = null;
      } else if (c === '"' || c === "'") quote = c;
      else if (c === "#" && (i === 0 || /\s/.test(line[i - 1])))
        return line.slice(0, i);
    }
    return line;
  }
  function splitKey(text) {
    let quote = null,
      depth = 0;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (quote) {
        if (c === quote && text[i - 1] !== "\\") quote = null;
      } else if (c === '"' || c === "'") quote = c;
      else if ("[{(".includes(c)) depth++;
      else if ("]})".includes(c)) depth--;
      else if (c === ":" && depth === 0)
        return [text.slice(0, i).trim(), text.slice(i + 1).trim()];
    }
    throw new ParseError(`Expected a key and value in '${text}'.`);
  }
  function parseYaml(text) {
    const lines = String(text)
      .replace(/\r/g, "")
      .split("\n")
      .map((raw, index) => ({
        index: index + 1,
        indent: (raw.match(/^ */) || [""])[0].length,
        text: stripComment(raw).trim(),
      }))
      .filter((x) => x.text);
    function block(start, indent) {
      if (start >= lines.length || lines[start].indent < indent)
        return [{}, start];
      const array = lines[start].text.startsWith("- "),
        out = array ? [] : {};
      let i = start;
      while (
        i < lines.length &&
        lines[i].indent === indent &&
        lines[i].text.startsWith("- ") === array
      ) {
        const row = lines[i],
          content = array ? row.text.slice(2).trim() : row.text;
        if (array) {
          if (!content) {
            const child = block(i + 1, lines[i + 1]?.indent ?? indent + 2);
            out.push(child[0]);
            i = child[1];
            continue;
          }
          if (content.includes(":")) {
            const pair = splitKey(content),
              item = {};
            item[pair[0]] = pair[1] ? scalar(pair[1]) : {};
            i++;
            while (i < lines.length && lines[i].indent > indent) {
              const childIndent = lines[i].indent;
              if (lines[i].text.startsWith("- ")) {
                const key = Object.keys(item).at(-1),
                  child = block(i, childIndent);
                item[key] = child[0];
                i = child[1];
                continue;
              }
              const p = splitKey(lines[i].text);
              if (p[1]) {
                item[p[0]] = scalar(p[1]);
                i++;
              } else {
                const child = block(
                  i + 1,
                  lines[i + 1]?.indent ?? childIndent + 2,
                );
                item[p[0]] = child[0];
                i = child[1];
              }
            }
            out.push(item);
            continue;
          }
          out.push(scalar(content));
          i++;
          continue;
        }
        const pair = splitKey(content);
        if (pair[1]) {
          out[pair[0]] = scalar(pair[1]);
          i++;
        } else if (i + 1 < lines.length && lines[i + 1].indent > indent) {
          const child = block(i + 1, lines[i + 1].indent);
          out[pair[0]] = child[0];
          i = child[1];
        } else {
          out[pair[0]] = {};
          i++;
        }
      }
      return [out, i];
    }
    return lines.length ? block(0, lines[0].indent)[0] : {};
  }
  function splitTop(text, separator = ",") {
    const out = [];
    let start = 0,
      depth = 0,
      quote = null,
      escaped = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (quote) {
        if (escaped) escaped = false;
        else if (c === "\\" && quote === '"') escaped = true;
        else if (c === quote) quote = null;
      } else if (c === '"' || c === "'") quote = c;
      else if ("([{ ".includes(c) && c !== " ") depth++;
      else if (")]}".includes(c)) depth--;
      else if (c === separator && depth === 0) {
        if (text.slice(start, i).trim()) out.push(text.slice(start, i).trim());
        start = i + 1;
      }
    }
    if (text.slice(start).trim()) out.push(text.slice(start).trim());
    return out;
  }
  function splitEquals(text) {
    let depth = 0,
      quote = null,
      escaped = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i];
      if (quote) {
        if (escaped) escaped = false;
        else if (c === "\\" && quote === '"') escaped = true;
        else if (c === quote) quote = null;
      } else if (c === '"' || c === "'") quote = c;
      else if ("([{ ".includes(c) && c !== " ") depth++;
      else if (")]}".includes(c)) depth--;
      else if (c === "=" && depth === 0)
        return [text.slice(0, i).trim(), text.slice(i + 1).trim()];
    }
    return null;
  }
  function vector(raw, line) {
    if (!(raw.startsWith("c(") && raw.endsWith(")")))
      throw new ParseError("Options and rows must use c(...).", line);
    return splitTop(raw.slice(2, -1)).map((item) => {
      const pair = splitEquals(item);
      if (!pair) {
        const value = scalar(item);
        return { label: String(value), value, _named: false };
      }
      const option = {
        label: String(scalar(pair[0])),
        value: scalar(pair[1]),
        _named: true,
      };
      if (
        /^[a-z][a-z0-9_]*$/.test(pair[0]) &&
        /^["']/.test(pair[1]) &&
        String(option.value).includes(" ")
      )
        option._looks_reversed = true;
      return option;
    });
  }
  function sequence(raw, line) {
    const match =
      /^seq\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)$/.exec(
        raw,
      );
    if (!match) return vector(raw, line);
    const start = Number(match[1]),
      stop = Number(match[2]),
      step = Number(match[3]);
    if (!step || (stop - start) * step < 0)
      throw new ParseError(
        "seq() needs a non-zero step that moves toward its endpoint.",
        line,
      );
    const result = [];
    for (
      let value = start;
      step > 0
        ? value <= stop + Math.abs(step) / 1e6
        : value >= stop - Math.abs(step) / 1e6;
      value += step
    ) {
      const normalized = Number(value.toFixed(12));
      result.push({ label: String(normalized), value: normalized });
      if (result.length > 10000)
        throw new ParseError("seq() creates too many slider values.", line);
    }
    return result;
  }
  function callArgs(body, line) {
    const found = CALL_RE.exec(body);
    if (!found) return [null, {}];
    let depth = 1,
      quote = null,
      escaped = false,
      end = -1;
    for (let i = found.index + found[0].length; i < body.length; i++) {
      const c = body[i];
      if (quote) {
        if (escaped) escaped = false;
        else if (c === "\\" && quote === '"') escaped = true;
        else if (c === quote) quote = null;
      } else if (c === '"' || c === "'") quote = c;
      else if (c === "(") depth++;
      else if (c === ")" && --depth === 0) {
        end = i;
        break;
      }
    }
    if (end < 0)
      throw new ParseError(
        `The ${found[1]} call is missing a closing parenthesis.`,
        line,
      );
    if (body.slice(end + 1).trim())
      throw new ParseError(
        "Only one supported call is allowed in each R block.",
        line,
      );
    const args = {};
    for (const item of splitTop(
      body.slice(found.index + found[0].length, end),
    )) {
      const pair = splitEquals(item);
      if (!pair)
        throw new ParseError(
          `Every ${found[1]} argument must have a name.`,
          line,
        );
      if (Object.hasOwn(args, pair[0]))
        throw new ParseError(
          `Argument '${pair[0]}' appears more than once.`,
          line,
        );
      args[pair[0]] =
        [
          "option",
          "options",
          "row",
          "rows",
          "image",
          "default",
          "selected",
          "column",
          "columns",
          "group",
          "groups",
        ].includes(pair[0]) && /^(?:c|seq)\(/.test(pair[1])
          ? sequence(pair[1], line)
          : scalar(pair[1]);
    }
    return [found[1], args];
  }
  function parseSurvey(qmdText, source = "survey.qmd") {
    const text = String(qmdText).replace(/\r/g, "");
    if (!text.startsWith("---\n"))
      throw new ParseError("The file must begin with YAML front matter.", 1);
    const close = text.indexOf("\n---", 4);
    if (close < 0)
      throw new ParseError("The YAML front matter is not closed.", 1);
    const front = parseYaml(text.slice(4, close));
    for(const namespace of ["theme-settings","survey-settings","system-messages"]) {
      const alias=namespace.replaceAll("-","_");
      if(Object.hasOwn(front,alias)) {if(Object.hasOwn(front,namespace))throw new ParseError("Do not repeat a settings namespace using aliases.",1);front[namespace]=front[alias];delete front[alias];}
      if(front[namespace] && typeof front[namespace]==="object" && !Array.isArray(front[namespace])) {
        const normalized={};
        for(const [original,value] of Object.entries(front[namespace])) {const key=original.replaceAll("_","-");if(Object.hasOwn(normalized,key))throw new ParseError("Do not repeat a setting using aliases.",1);normalized[key]=value;}
        front[namespace]=normalized;
      }
    }
    const body = text.slice(close + 4).replace(/^\n+/, "");
    const matches = [...body.matchAll(PAGE_RE)];
    if (!matches.length)
      throw new ParseError(
        "No survey pages were found. Add a line such as '--- welcome'.",
      );
    const pages = [];
    for (let index = 0; index < matches.length; index++) {
      const match = matches[index],
        section = body.slice(
          match.index + match[0].length,
          index + 1 < matches.length ? matches[index + 1].index : body.length,
        );
      let plain = section.replace(FENCE_RE, "");
      const heading = /^#\s+(.+?)\s*$/m.exec(plain),
        title = heading
          ? heading[1].trim()
          : match[1]
              .replaceAll("_", " ")
              .replace(/\b\w/g, (c) => c.toUpperCase());
      if (heading)
        plain =
          plain.slice(0, heading.index) +
          plain.slice(heading.index + heading[0].length);
      plain = plain
        .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
        .replace(/\n{3,}/g, "\n\n")
        .trim();
      const page = { id: match[1], title, body: plain, questions: [] };
      const base =
        text.slice(0, close + 4).split("\n").length +
        body.slice(0, match.index + match[0].length).split("\n").length -
        1;
      for (const fence of section.matchAll(FENCE_RE)) {
        const line = base + section.slice(0, fence.index).split("\n").length;
        const [name, args0] = callArgs(fence[1].trim(), line),
          args = { ...args0 };
        if (name === "sd_question") {
          const q = {
            id: args.id ?? null,
            type: args.type ?? null,
            label: args.label ?? null,
            _line: line,
          };
          delete args.id;
          delete args.type;
          delete args.label;
          if (args.option) q.options = args.option;
          if (args.options && !q.options) q.options = args.options;
          if (args.row) q.rows = args.row;
          if (args.rows) q.rows = args.rows;
          if (args.column) q.columns = args.column;
          if (args.columns) q.columns = args.columns;
          if (args.group) q.groups = args.group;
          if (args.groups) q.groups = args.groups;
          if (args.image) q.images = args.image.map((item) => item.value);
          if (["mc_image", "mc_multiple_image"].includes(q.type))
            for (const option of q.options || [])
              option.caption = option._named !== false;
          for (const option of [...(q.options || []), ...(q.rows || []), ...(q.columns || []), ...(q.groups || [])])
            delete option._named;
          if (args.label_select) q.placeholder = args.label_select;
          for (const key of [
            "option",
            "options",
            "row",
            "rows",
            "label_select",
            "image",
            "column",
            "columns",
            "group",
            "groups",
          ])
            delete args[key];
          for (const key of [
            "placeholder",
            "min",
            "max",
            "step",
            "orientation",
            "direction",
            "status",
            "width",
            "height",
            "selected",
            "default",
            "grid",
            "individual",
            "justified",
            "force_edges",
            "resize",
            "cols",
            "matrix_question_width",
            "mobile_columns",
            "pre",
            "sep",
            "animate",
            "src",
            "poster",
            "caption",
            "transcript",
            "controls",
            "autoplay",
            "muted",
            "loop",
            "preload",
            "total",
            "path_separator",
            "low_label",
            "high_label",
            "base_type",
            "customization",
            "custom_class",
            "selection_hint",
          ]) {
            if (Object.hasOwn(args, key)) {
              q[key] =
                ["default", "selected"].includes(key) &&
                Array.isArray(args[key])
                  ? args[key].map((item) => item.value)
                  : args[key];
              delete args[key];
            }
          }
          if (Object.keys(args).length)
            q.unsupported_arguments = Object.keys(args).sort();
          page.questions.push(q);
        } else if (name === "sd_nav") {
          page.nav = args;
          page._nav_line = line;
        } else if (fence[1].trim())
          throw new ParseError(
            "This R block does not contain sd_question() or sd_nav().",
            line,
          );
      }
      pages.push(page);
    }
    return { front_matter: front, pages, source };
  }
  const issue = (code, message, file, line) =>
    Object.assign(
      { code, severity: "error", message, file },
      line ? { line } : {},
    );
  function validateSurvey(
    parsed,
    config,
    qmd = "survey.qmd",
    yml = "greedyq.yml",
  ) {
    const issues = [],
      pages = parsed.pages || [],
      pageIds = pages.map((p) => p.id),
      questions = pages.flatMap((p) => p.questions || []),
      qids = questions.map((q) => q.id),
      knownP = new Set(pageIds),
      knownQ = new Set(qids);
    try{prolificPlan(config);}catch(e){issues.push(issue('GQ020',e.message,yml));}
    if (parsed.front_matter?.greedyq?.spec_version !== "0.2")
      issues.push(
        issue("GQ003", "Set the survey specification version to 0.2.", qmd, 1),
      );
    if (config.spec_version !== "0.2")
      issues.push(
        issue("GQ003", "Set the study settings version to 0.2.", yml, 1),
      );
    const greedyqVersion = parsed.front_matter?.greedyq?.version;
    if (
      typeof greedyqVersion !== "string" ||
      !/^0\.2_\d{4}-\d{2}-\d{2}_[0-9a-f]{7,12}$/.test(greedyqVersion)
    )
      issues.push(
        issue(
          "GQ003",
          "Set greedyq.version to the exact release identifier shown at the top of the greedyQ repository (for example, 0.2_2026-09-09_abcdef0).",
          qmd,
          1,
        ),
      );
    const organization = parsed.front_matter?.greedyq?.organization;
    if(!LANGUAGES.includes(parsed.front_matter?.greedyq?.language ?? 'en'))issues.push(issue('GQ003','Choose en, ko, zh-CN or zh-TW for greedyq.language.',qmd,1));
    if (
      organization != null &&
      (typeof organization !== "string" ||
        !organization.trim() ||
        organization.length > 120)
    )
      issues.push(
        issue(
          "GQ003",
          "Set greedyq.organization to the researcher-facing organization or team name (1–120 characters).",
          qmd,
          1,
        ),
      );
    for (const id of new Set(pageIds.filter((x, i, a) => a.indexOf(x) !== i)))
      issues.push(
        issue("GQ001", `The page name '${id}' is used more than once.`, qmd),
      );
    for (const id of new Set(qids.filter((x, i, a) => x && a.indexOf(x) !== i)))
      issues.push(
        issue(
          "GQ001",
          `The question name '${id}' is used more than once.`,
          qmd,
        ),
      );
    for (const p of pages) {
      if (/<\s*\/?\s*[A-Za-z][^>]*>/.test(p.body || ""))
        issues.push(issue("GQ003", `Page '${p.id}' contains raw HTML.`, qmd));
      const target = p.nav?.page_next;
      if (target && !knownP.has(target))
        issues.push(
          issue(
            "GQ002",
            `Page '${p.id}' continues to missing page '${target}'.`,
            qmd,
            p._nav_line,
          ),
        );
    }
    for (const q of questions) {
      if (!q.id) {
        issues.push(
          issue("GQ001", "A question is missing its id.", qmd, q._line),
        );
        continue;
      }
      if (!ID_RE.test(String(q.id)))
        issues.push(
          issue("GQ001", `The question id '${q.id}' is invalid.`, qmd, q._line),
        );
      if (!q.type || !TYPES.has(q.type))
        issues.push(
          issue(
            "GQ003",
            `Question '${q.id}' uses a missing or unsupported type.`,
            qmd,
            q._line,
          ),
        );
      if (!q.label)
        issues.push(
          issue(
            "GQ003",
            `Question '${q.id}' needs participant-facing wording in label.`,
            qmd,
            q._line,
          ),
        );
      if (
        [
          "mc",
          "mc_multiple",
          "mc_buttons",
          "mc_multiple_buttons",
          "mc_image",
          "mc_multiple_image",
          "select",
          "slider",
          "matrix",
          "matrix_multiple",
        ].includes(q.type) &&
        !q.options?.length
      )
        issues.push(
          issue(
            "GQ003",
            `Question '${q.id}' needs at least one answer choice.`,
            qmd,
            q._line,
          ),
        );
      if (["matrix", "matrix_multiple"].includes(q.type) && !q.rows?.length)
        issues.push(
          issue(
            "GQ003",
            `Matrix question '${q.id}' needs at least one row.`,
            qmd,
            q._line,
          ),
        );
      if (
        ["matrix", "matrix_multiple"].includes(q.type) &&
        ![2, 3].includes(q.mobile_columns ?? 3)
      )
        issues.push(
          issue(
            "GQ003",
            `Matrix question '${q.id}' mobile_columns must be 2 or 3.`,
            qmd,
            q._line,
          ),
        );
      if (["audio", "video"].includes(q.type) && !q.src)
        issues.push(
          issue(
            "GQ003",
            `Media control '${q.id}' needs a safe source in src.`,
            qmd,
            q._line,
          ),
        );
      if (
        ["rank_order", "constant_sum", "pick_group_rank", "drill_down"].includes(q.type) &&
        (q.options || []).length < 2
      )
        issues.push(issue("GQ003", `Question '${q.id}' needs at least two items.`, qmd, q._line));
      if (
        q.type === "side_by_side" &&
        (!(q.rows || []).length || !(q.options || []).length || !(q.columns || []).length)
      )
        issues.push(issue("GQ003", `Side-by-side question '${q.id}' needs rows, columns, and answer choices.`, qmd, q._line));
      if (q.type === "pick_group_rank" && (q.groups || []).length < 2)
        issues.push(issue("GQ003", `Pick, group, and rank question '${q.id}' needs at least two groups.`, qmd, q._line));
      if (q.type === "constant_sum" && (!(typeof (q.total ?? 100) === "number") || (q.total ?? 100) <= 0))
        issues.push(issue("GQ003", `Constant-sum question '${q.id}' needs a positive total.`, qmd, q._line));
      if (
        q.type === "custom" &&
        (!TYPES.has(q.base_type) || ["custom", "timing", "audio", "video"].includes(q.base_type))
      )
        issues.push(issue("GQ003", `Custom question '${q.id}' must name a supported response control in base_type.`, qmd, q._line));
      if (
        ["mc_image", "mc_multiple_image"].includes(q.type) &&
        (q.images || []).length !== (q.options || []).length
      )
        issues.push(
          issue(
            "GQ003",
            `Image question '${q.id}' needs exactly one image for each answer choice.`,
            qmd,
            q._line,
          ),
        );
      if (![null, undefined, "horizontal", "vertical"].includes(q.direction))
        issues.push(
          issue(
            "GQ003",
            `Question '${q.id}' uses an unsupported button direction.`,
            qmd,
            q._line,
          ),
        );
      if (
        ![null, undefined, "none", "both", "horizontal", "vertical"].includes(
          q.resize,
        )
      )
        issues.push(
          issue(
            "GQ003",
            `Question '${q.id}' uses an unsupported textarea resize setting.`,
            qmd,
            q._line,
          ),
        );
      for (const dimension of ["width", "height"])
        if (
          q[dimension] != null &&
          !/^\d+(?:\.\d+)?(?:px|%|rem|em|vw|vh)$/.test(String(q[dimension]))
        )
          issues.push(
            issue(
              "GQ003",
              `Question '${q.id}' needs a safe CSS ${dimension}.`,
              qmd,
              q._line,
            ),
          );
      for (const image of q.images || [])
        if (
          !(
            String(image).startsWith("https://") ||
            /^(?!\/)(?!.*\.\.)[A-Za-z0-9_./-]+$/.test(String(image))
          )
        )
          issues.push(
            issue(
              "GQ003",
              `Image question '${q.id}' contains an unsafe image path.`,
              qmd,
              q._line,
            ),
          );
      for (const mediaKey of ["src", "poster"]) {
        const media = q[mediaKey];
        if (
          media != null &&
          !(
            String(media).startsWith("https://") ||
            /^(?!\/)(?!.*\.\.)[A-Za-z0-9_./-]+$/.test(String(media))
          )
        )
          issues.push(
            issue(
              "GQ003",
              `Media control '${q.id}' contains an unsafe ${mediaKey} path.`,
              qmd,
              q._line,
            ),
          );
      }
      if (["audio", "video"].includes(q.type) && q.autoplay && !q.muted)
        issues.push(
          issue(
            "GQ003",
            `Media control '${q.id}' may autoplay only when muted.`,
            qmd,
            q._line,
          ),
        );
      if (
        q.type === "slider_numeric" &&
        Array.isArray(q.default) &&
        ![1, 2].includes(q.default.length)
      )
        issues.push(
          issue(
            "GQ003",
            `Numeric slider '${q.id}' default must contain one value or two range endpoints.`,
            qmd,
            q._line,
          ),
        );
      if (q.type === "slider" && (q.options || []).length < 2)
        issues.push(
          issue(
            "GQ003",
            `Slider question '${q.id}' needs at least two ordered choices.`,
            qmd,
            q._line,
          ),
        );
      if (
        q.type === "slider_numeric" &&
        q.min != null &&
        q.max != null &&
        q.min >= q.max
      )
        issues.push(
          issue(
            "GQ003",
            `Numeric slider '${q.id}' needs a maximum greater than its minimum.`,
            qmd,
            q._line,
          ),
        );
      if (![null, undefined, "horizontal", "vertical"].includes(q.orientation))
        issues.push(
          issue(
            "GQ003",
            `Question '${q.id}' uses an unsupported slider orientation.`,
            qmd,
            q._line,
          ),
        );
      if (
        [...(q.options || []), ...(q.rows || [])].some((x) => x._looks_reversed)
      )
        issues.push(
          issue(
            "GQ011",
            `Question '${q.id}' appears to reverse displayed labels and stored values.`,
            qmd,
            q._line,
          ),
        );
      for (const arg of q.unsupported_arguments || [])
        issues.push(
          issue(
            "GQ003",
            `Question '${q.id}' uses unsupported argument '${arg}'.`,
            qmd,
            q._line,
          ),
        );
    }
    for (const p of pages) {
      for (const key of ["previous_mode", "next_mode"])
        if (![undefined, null, "show", "hide", "disable"].includes(p.nav?.[key]))
          issues.push(
            issue(
              "GQ003",
              `Page '${p.id}' uses an unsupported ${key}. Choose show, hide, or disable.`,
              qmd,
              p._nav_line,
            ),
          );
      const delay = p.nav?.next_delay_seconds ?? 0;
      if (typeof delay !== "number" || delay < 0 || delay > 86400)
        issues.push(
          issue(
            "GQ003",
            `Page '${p.id}' needs next_delay_seconds between 0 and 86400.`,
            qmd,
            p._nav_line,
          ),
        );
    }
    const settings = parsed.front_matter?.["survey-settings"] || {},
      start = settings["start-page"] || pageIds[0];
    if (!knownP.has(start))
      issues.push(
        issue("GQ002", `The starting page '${start}' does not exist.`, qmd),
      );
    for (const id of settings.required || [])
      if (!knownQ.has(id))
        issues.push(
          issue(
            "GQ002",
            `The required-question list refers to '${id}', but it does not exist.`,
            qmd,
          ),
        );
    for (const rule of config.logic?.show || []) {
      const target = rule.question || rule.page;
      if (!(rule.question ? knownQ : knownP).has(target))
        issues.push(
          issue(
            "GQ002",
            `A display rule refers to '${target}', but it does not exist.`,
            yml,
          ),
        );
    }
    for (const rule of config.logic?.skip || []) {
      if (!knownP.has(rule.from))
        issues.push(
          issue(
            "GQ002",
            `A route starts from missing page '${rule.from}'.`,
            yml,
          ),
        );
      if (!knownP.has(rule.to))
        issues.push(
          issue("GQ002", `A route points to missing page '${rule.to}'.`, yml),
        );
    }
    for (const [name, outcome] of Object.entries(config.outcomes || {}))
      if (!knownP.has(outcome.page))
        issues.push(
          issue(
            "GQ002",
            `The '${name}' ending points to missing page '${outcome.page}'.`,
            yml,
          ),
        );
    const errors = issues.filter((x) => x.severity === "error");
    return {
      schema_version: "0.2",
      status: errors.length ? "failed" : "passed",
      summary: `${errors.length} error(s), ${issues.length - errors.length} warning(s)`,
      issues,
    };
  }
  function validateSurveyComplete(
    parsed,
    config,
    qmd = "survey.qmd",
    yml = "greedyq.yml",
  ) {
    if ((Object.hasOwn(config,"randomization") && !Array.isArray(config.randomization)) || (config.randomization || []).some(r=>!r || typeof r!=="object" || Array.isArray(r)))
      return {schema_version:"0.2",status:"failed",summary:"1 error(s), 0 warning(s)",issues:[issue("GQ007","randomization must be a list of assignment objects.",yml)]};
    if ((config.randomization || []).some(r=>["conditions","store","assignment_point"].some(k=>Object.hasOwn(r,k) && (!r[k] || typeof r[k]!=="object" || Array.isArray(r[k])))))
      return {schema_version:"0.2",status:"failed",summary:"1 error(s), 0 warning(s)",issues:[issue("GQ007","Random assignment conditions, store, and assignment_point must be objects.",yml)]};
    const report = validateSurvey(parsed, config, qmd, yml),
      issues = report.issues,
      pages = parsed.pages || [],
      questions = pages.flatMap((page) => page.questions || []),
      pageIds = new Set(pages.map((page) => page.id)),
      questionIds = new Set(questions.map((question) => question.id));
    const frontKeys = new Set([
        "title",
        "greedyq",
        "theme-settings",
        "survey-settings",
        "system-messages",
      ]),
      namespaceKeys = {
        greedyq: new Set(["spec_version", "version", "organization", "language"]),
        "theme-settings": new Set([
          "theme",
          "barposition",
          "barcolor",
          "footer",
          "footer-left",
          "footer-center",
          "footer-right",
        ]),
        "survey-settings": new Set([
          "show-previous",
          "use-cookies",
          "all-required",
          "start-page",
          "highlight-unanswered",
          "capture-metadata",
          "required",
          "shuffled",
          "all-shuffled",
        ]),
        "system-messages": new Set(["previous", "next", "required"]),
      };
    for (const key of Object.keys(parsed.front_matter || {}))
      if (!frontKeys.has(key))
        issues.push(
          issue(
            "GQ003",
            `The survey header uses '${key}', which is not a supported setting.`,
            qmd,
            1,
          ),
        );
    for(const [namespace,defaults] of Object.entries({'theme-settings':{theme:'default',barposition:'top',footer:'','footer-left':'','footer-center':'','footer-right':''},'survey-settings':{'use-cookies':true,'highlight-unanswered':false,'capture-metadata':false}}))
      for(const [key,value] of Object.entries(defaults))if(Object.hasOwn(parsed.front_matter?.[namespace] || {},key) && parsed.front_matter[namespace][key]!==value)issues.push({...issue('GQ120',`Setting '${namespace}.${key}' is not fully implemented in the browser runtime; review the compatibility audit.`,qmd),severity:'warning'});
    for (const [name, allowed] of Object.entries(namespaceKeys))
      for (const key of Object.keys(parsed.front_matter?.[name] || {}))
        if (!allowed.has(key))
          issues.push(
            issue(
              "GQ003",
              `The '${name}' section uses the unsupported setting '${key}'.`,
              qmd,
              1,
            ),
          );
    for (const id of pageIds)
      if (questionIds.has(id))
        issues.push(
          issue(
            "GQ001",
            `'${id}' is used for both a page and a question. Use a different name for one of them.`,
            qmd,
          ),
        );
    for (const q of questions)
      for (const collection of ["options", "rows", "columns", "groups"]) {
        const values = (q[collection] || []).map((item) => String(item.value));
        if (new Set(values).size !== values.length)
          issues.push(
            issue(
              "GQ011",
              `Question '${q.id}' repeats a stored value in its ${collection}. Every stored value must be unique.`,
              qmd,
              q._line,
            ),
          );
      }
    const storedValues = new Map(
        questions.map((q) => [q.id, new Set((q.options || []).map((item) => String(item.value)))]),
      ),
      derivedFields = new Set(
        (config.randomization || []).map((item) => item.store?.condition_as).filter(Boolean),
      ),
      checkCondition = (expression,ruleId) => {
        const before=issues.length;
        const inspect=node=>{
          if(node.all || node.any)(node.all || node.any).forEach(inspect);
          else if(node.not)inspect(node.not);
          else if(node.unsupported!==undefined || !/^[a-z][a-z0-9_]*$/.test(node.field || '') || ['lt','lte','gt','gte'].some(k=>k in node && typeof node[k]!=='number'))issues.push(issue('GQ011','Use a supported condition, for example contains(tools, "other"), length(tools) >= 2, age >= 18 or answered(question). Arbitrary expressions are not executed.',yml));
          else if(!questionIds.has(node.field) && !derivedFields.has(node.field) && node.field!=='condition')issues.push(issue('GQ011',`A condition refers to '${node.field}', but that question does not exist.`,yml));
          if(node.length && (typeof node.length!=='object'||Object.values(node.length).some(v=>typeof v!=='number')))issues.push(issue('GQ011','length() must compare a collection length with a number.',yml));
          if('contains'in node || 'in'in node){const values=node.in??[node.contains];if(!Array.isArray(values)||values.some(v=>v!==null&&typeof v==='object'))issues.push(issue('GQ011','Membership requires scalar stored values.',yml));else if(storedValues.get(node.field)?.size)for(const value of values)if(value!==null&&!storedValues.get(node.field).has(String(value)))issues.push(issue('GQ011',`A condition compares '${node.field}' with '${value}', which is not one of its stored answer values.`,yml));}
          if(node.length){const q=questions.find(q=>q.id===node.field)||{};if(!['text','textarea','mc_multiple','mc_multiple_buttons','mc_multiple_image','select_multiple','slider','date'].includes(q.type==='custom'?q.base_type:q.type))issues.push(issue('GQ011','length() requires text or a multiple-selection question.',yml));}
          if('contains'in node){const q=questions.find(q=>q.id===node.field)||{};if(!['mc_multiple','mc_multiple_buttons','mc_multiple_image','select_multiple'].includes(q.type==='custom'?q.base_type:q.type))issues.push(issue('GQ011','contains() requires a multiple-selection question.',yml));}
        };inspect(condition(expression));
        const pattern = /\b([a-z][a-z0-9_]*)\s*(?:==|!=)\s*['"]([^'"]+)['"]/g;
        for (const match of String(expression || "").matchAll(pattern)) {
          const [, field, literal] = match;
          if (!questionIds.has(field) && !derivedFields.has(field))
            issues.push(issue("GQ011", `A condition refers to '${field}', but that question does not exist.`, yml));
          else if (storedValues.get(field)?.size && !storedValues.get(field).has(literal))
            issues.push(issue("GQ011", `A condition compares '${field}' with '${literal}', which is not one of its stored answer values.`, yml));
        }
        if(ruleId)for(const item of issues.slice(before))item.message=`Rule '${ruleId}': ${item.message}`;
      };
    for (const rule of config.logic?.show || []) checkCondition(rule.if,rule.id||rule.question||rule.from);
    for (const rule of config.logic?.skip || []) checkCondition(rule.if,rule.id||rule.question||rule.from);
    for(const rule of config.logic?.validate || []) {checkCondition(rule.if,rule.id||rule.question||rule.from);if(!questionIds.has(rule.question))issues.push(issue('GQ002','A validation rule refers to a missing question.',yml));}
    if ((config.randomization || []).length > 1)
      issues.push(issue("GQ007", "Only one between-subject random assignment is supported per study.", yml));
    for (const randomization of config.randomization || []) {
      const problem = planProblem(randomization);
      if (problem) issues.push(issue("GQ007", problem, yml));
      const after = randomization.assignment_point?.after_page;
      if (!pageIds.has(after))
        issues.push(
          issue(
            "GQ002",
            `Random assignment refers to missing page '${after}'.`,
            yml,
          ),
        );
      if (Object.keys(randomization.conditions || {}).length < 2)
        issues.push(
          issue(
            "GQ007",
            `Random assignment '${randomization.id}' needs at least two conditions.`,
            yml,
          ),
        );
      if (!randomization.persistence_key || !randomization.store?.condition_as)
        issues.push(
          issue(
            "GQ007",
            `Random assignment '${randomization.id}' must save each participant's condition so it cannot change on resume.`,
            yml,
          ),
        );
    }
    for (const problem of [...boundaryProblems(parsed, config), ...orderingProblems(parsed, config)]) issues.push(issue("GQ007", problem, yml));
    try { optionPlan(parsed); } catch (e) { issues.push(issue("GQ007", e.message, qmd)); }
    try { pagePlan(parsed,config); } catch (e) { issues.push(issue("GQ007", e.message, yml)); }
    const consent = config.consent;
    if (consent) {
      const q = questions.find(
        (item) => item.id === consent.confirmation_question,
      );
      if (!q)
        issues.push(
          issue(
            "GQ006",
            `Consent refers to missing question '${consent.confirmation_question}'.`,
            yml,
          ),
        );
      else if (
        !(q.options || []).some(
          (option) => option.value === consent.accept_value,
        )
      )
        issues.push(
          issue(
            "GQ006",
            `The configured consent answer '${consent.accept_value}' is not an option in question '${q.id}'.`,
            yml,
          ),
        );
    }
    for (const [name, outcome] of Object.entries(config.outcomes || {})) {
      try {redirectPlan(outcome);} catch(e) {issues.push(issue("GQ009",e.message,yml));}
      if (outcome.redirect && !String(outcome.redirect).startsWith("https://"))
        issues.push(
          issue(
            "GQ009",
            `The '${name}' redirect must use a secure https address.`,
            yml,
          ),
        );
    }
    const unique = new Map();
    for (const item of issues)
      unique.set(
        [item.code, item.file, item.line || 0, item.message].join("|"),
        item,
      );
    report.issues = [...unique.values()];
    const errors = report.issues.filter((item) => item.severity === "error");
    report.status = errors.length ? "failed" : "passed";
    report.summary = `${errors.length} error(s), ${report.issues.length - errors.length} warning(s)`;
    return report;
  }
  const OPS = [
    ["!=", "not_equals"],
    ["<=", "lte"],
    [">=", "gte"],
    ["==", "equals"],
    ["<", "lt"],
    [">", "gt"],
  ];
  function condition(expression, depth=0) {
    const original=String(expression).trim();let s=original;
    if(depth>64 || s.length>4096)return {unsupported:original};
    const split=(text,separator)=>{let quote=null,escaped=false,level=0,start=0;const parts=[];for(let i=0;i<text.length;i++){const c=text[i];if(escaped){escaped=false;continue;}if(quote){if(c==='\\')escaped=true;else if(c===quote)quote=null;continue;}if(c==='"'||c==="'"){quote=c;continue;}if(c==='('||c==='[')level++;else if(c===')'||c===']')level--;else if(level===0&&text.startsWith(separator,i)){parts.push(text.slice(start,i));start=i+separator.length;i+=separator.length-1;}}parts.push(text.slice(start));return parts;};
    while(s.startsWith('(')&&s.endsWith(')')){let level=0,quote=null,escaped=false,whole=true;for(let i=0;i<s.length;i++){const c=s[i];if(escaped){escaped=false;continue;}if(quote){if(c==='\\')escaped=true;else if(c===quote)quote=null;continue;}if(c==='"'||c==="'")quote=c;else if(c==='(')level++;else if(c===')'&&--level===0&&i<s.length-1){whole=false;break;}}if(!whole||level!==0)break;s=s.slice(1,-1).trim();}
    const literal=text=>{text=text.trim();if(text.startsWith('[')&&text.endsWith(']'))return text.slice(1,-1).trim()?split(text.slice(1,-1),',').map(literal):[];if(/^"(?:\\.|[^"\\])*"$/.test(text))return JSON.parse(text);if(/^'(?:\\.|[^'\\])*'$/.test(text))return text.slice(1,-1).replace(/\\(['\\])/g,'$1').replace(/\\n/g,'\n');if(/^-?(?:\d+(?:\.\d*)?|\.\d+)$/.test(text))return Number(text);if(/^[a-z][a-z0-9_]*$/.test(text))return ({true:true,false:false,null:null})[text]??(text==='null'?null:text);throw Error('literal');};
    const field=name=>name==='assignment_condition'?'condition':name;
    for(const [connector,key] of [[' or ','any'],[' and ','all']]){const parts=split(s,connector);if(parts.length>1)return {[key]:parts.map(p=>condition(p,depth+1))};}
    if(s.startsWith('not ')){const child=condition(s.slice(4),depth+1);return 'answered'in child?{...child,answered:!child.answered}:{not:child};}
    const answered=/^answered\(\s*([a-z][a-z0-9_]*)\s*\)$/.exec(s);if(answered)return {field:field(answered[1]),answered:true};
    try {
      let match=/^contains\(\s*([a-z][a-z0-9_]*)\s*,\s*(.+)\)$/.exec(s);if(match)return {field:field(match[1]),contains:literal(match[2])};
      match=/^([a-z][a-z0-9_]*)\s+(not in|in)\s+(.+)$/.exec(s);if(match){const list=literal(match[3]);if(!Array.isArray(list))throw Error('membership');const node={field:field(match[1]),in:list};return match[2]==='not in'?{not:node}:node;}
      match=/^(?:length\(\s*([a-z][a-z0-9_]*)\s*\)|([a-z][a-z0-9_]*))\s*(==|!=|<=|>=|<|>)\s*(.+)$/.exec(s);
      if(match){const key=OPS.find(([token])=>token===match[3])[1],value=literal(match[4]);if(Array.isArray(value))throw Error('scalar');return match[1]?{field:field(match[1]),length:{[key]:value}}:{field:field(match[2]),[key]:value};}
    }catch{}
    return {unsupported:original};
  }
  function matchesCondition(rule, answers, assigned) {
    if(!rule)return true;
    if(rule.all)return rule.all.every(r=>matchesCondition(r,answers,assigned));
    if(rule.any)return rule.any.some(r=>matchesCondition(r,answers,assigned));
    if(rule.not)return !matchesCondition(rule.not,answers,assigned);
    const actual=rule.field==='condition'?assigned:answers[rule.field];
    const equal=(a,b)=>typeof a===typeof b && a===b;
    if('answered'in rule)return (actual!=null&&actual!==''&&(!Array.isArray(actual)||actual.length>0)&&(!(actual&&typeof actual==='object'&&!Array.isArray(actual))||Object.keys(actual).length>0))===rule.answered;
    if('contains'in rule)return Array.isArray(actual)&&actual.some(v=>equal(v,rule.contains));
    if('in'in rule)return actual!=null&&rule.in.some(v=>equal(actual,v));
    const compare=(value,node)=>{
      if('equals'in node)return equal(value??null,node.equals);
      if(value==null)return false;
      if('not_equals'in node)return node.not_equals!=null&&!equal(value,node.not_equals);
      for(const [key,fn] of [['lt',(a,b)=>a<b],['lte',(a,b)=>a<=b],['gt',(a,b)=>a>b],['gte',(a,b)=>a>=b]])if(key in node)return typeof value==='number'&&typeof node[key]==='number'&&fn(value,node[key]);
      return false;
    };
    if(rule.length){if(typeof actual!=='string'&&!Array.isArray(actual))return false;return compare(typeof actual==='string'?Array.from(actual).length:actual.length,rule.length);}
    return compare(actual,rule);
  }
  function compileSurvey(parsed, config) {
    const prolific=prolificPlan(config);
    const optionPlans=optionPlan(parsed);
    const predicate=expression=>{
      for(const r of config.randomization || []) if(r.store?.condition_as)
        expression=String(expression).replace(new RegExp("\\b"+r.store.condition_as.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")+"\\b","g"),"assignment_condition");
      return condition(expression);
    };
    const front = parsed.front_matter,
      settings = front["survey-settings"] || {},
      required = new Set(settings.required || []),
      shows = config.logic?.show || [],
      validations = config.logic?.validate || [],
      skips = [...(config.logic?.skip || [])].sort(
        (a, b) => (b.priority || 0) - (a.priority || 0),
      ),
      outcomes = config.outcomes || {},
      term = Object.fromEntries(
        Object.entries(outcomes).map(([key, v]) => [
          v.page,
          v.lifecycle_state || key,
        ]),
      );
    const pages = parsed.pages.map((source, index) => {
      const page = {
        id: source.id,
        title: source.title,
        body: source.body,
        questions: source.questions.map((s) => {
          const q = Object.fromEntries(
            Object.entries(s).filter(
              ([k]) => !k.startsWith("_") && k !== "unsupported_arguments",
            ),
          );
          for (const key of ["options", "rows"])
            if (q[key])
              q[key] = q[key].map((x) =>
                Object.fromEntries(
                  Object.entries(x).filter(([k]) => !k.startsWith("_")),
                ),
              );
          q.required = !!settings["all-required"] || required.has(q.id);
          if(Object.hasOwn(optionPlans,q.id)) q.shuffle_items=optionPlans[q.id];
          const show = shows.find((x) => x.question === q.id);
          if (show) q.show_if = predicate(show.if);
          for (const rule of validations.filter((x) => x.question === q.id)) {
            const expression = String(rule.if || ""),
              exact = new RegExp(
                `^\\s*${q.id}\\s*>\\s*(-?\\d+(?:\\.\\d+)?)\\s*$`,
              ).exec(expression),
              low = new RegExp(`${q.id}\\s*<\\s*(-?\\d+(?:\\.\\d+)?)`).exec(
                expression,
              ),
              high = new RegExp(`${q.id}\\s*>\\s*(-?\\d+(?:\\.\\d+)?)`).exec(
                expression,
              );
            if (exact) q.max = Number(exact[1]);
            if (low && high) {
              q.min = Number(low[1]);
              q.max = Number(high[1]);
            }
            if (expression.includes(`not answered(${q.id})`)) q.required = true;
          }
          if (q.id === "age" && q.type === "numeric" && q.min == null)
            q.min = 0;
          return q;
        }),
      };
      const nav = source.nav || {};
      page.show_previous = Boolean(
        nav.show_previous ?? settings["show-previous"] ?? true,
      );
      page.previous_mode =
        nav.previous_mode ?? (page.show_previous ? "show" : "hide");
      page.next_mode =
        nav.next_mode ?? (nav.show_next === false ? "hide" : "show");
      page.next_delay_seconds = nav.next_delay_seconds ?? 0;
      page.next = nav.page_next || (parsed.pages[index + 1]?.id ?? null);
      if (nav.label_next) page.next_label = nav.label_next;
      const routes = skips
        .filter((x) => x.from === page.id)
        .map((x) => ({ when: predicate(x.if), to: x.to }));
      if (routes.length) page.routes = routes;
      for(const rule of shows)if(rule.page===page.id)page.show_if=predicate(rule.if || "");
      const checks=validations.filter(r=>page.questions.some(q=>q.id===r.question)).map(r=>({question:r.question,when:predicate(r.if || ""),message:r.message || translate(front.greedyq?.language || "en","Please review this answer.")}));
      if(checks.length)page.checks=checks;
      if (term[page.id]) {
        delete page.next;
        page.terminal = term[page.id];
        const redirect=redirectPlan(Object.values(outcomes).find(o=>o.page===page.id));
        if(redirect)page.redirect=redirect;
      }
      return page;
    });
    for (const rule of config.question_order || [])
      pages.find(p => p.id === rule.page).shuffle_questions = [...rule.questions];
    const random = config.randomization?.[0],
      conditions = random ? Object.keys(random.conditions || {}) : ["default"],
      start = settings["start-page"] || pages[0].id,
      byId = new Map(pages.map((p) => [p.id, p])),
      paths = {};
    for (const assigned of conditions.length ? conditions : ["default"]) {
      const path = [];
      let current = start;
      while (byId.has(current) && !path.includes(current)) {
        path.push(current);
        const p = byId.get(current);
        if (p.terminal) break;
        current =
          (p.routes || []).find(
            (r) => r.when.field === "condition" && r.when.equals === assigned,
          )?.to ?? p.next;
      }
      paths[assigned] = path;
    }
    return {
      study_id: config.study?.id || "greedyq_preview",
      study_version: config.study?.version || "unknown",
      greedyq_version: front.greedyq?.version,
      title: config.study?.title || front.title || translate(front.greedyq?.language || "en","greedyQ Survey"),
      organization: front.greedyq?.organization || translate(front.greedyq?.language || "en","Research team"),
      language: front.greedyq?.language || 'en',
      start_page: start,
      brand_color: front["theme-settings"]?.barcolor || "#315c8a",
      messages: {
        previous: front["system-messages"]?.previous || translate(front.greedyq?.language || 'en', "Previous"),
        next: front["system-messages"]?.next || translate(front.greedyq?.language || 'en', "Continue"),
        required:
          front["system-messages"]?.required ||
          translate(front.greedyq?.language || 'en', "Please answer the required questions before continuing."),
      },
      conditions: conditions.length ? conditions : ["default"],
      ...(random ? {randomization: random} : {}),
      progress_paths: paths,
      ...(pagePlan(parsed,config).length ? {shuffle_pages:pagePlan(parsed,config)} : {}),
      pages,
      runtime_policy: {
        ...(prolific?{prolific}:{}),
        mode: config.respondents?.mode || "test",
        consent: config.consent
          ? {
              question: config.consent.confirmation_question,
              accept_value: config.consent.accept_value,
              refusal_outcome: config.consent.refusal_outcome,
            }
          : null,
        respondent_source: config.respondents?.source || "direct_link",
        duplicate_policy: config.respondents?.duplicate_policy || "resume",
      },
      ...(random?.assignment_point?.after_page
        ? { assignment_page: random.assignment_point.after_page }
        : {}),
    };
  }
  function detectDevice(win = window) {
    const mobile =
      win.matchMedia?.("(max-width: 700px), (pointer: coarse)").matches ||
      (win.navigator.maxTouchPoints > 0 && win.innerWidth < 900);
    return mobile ? "mobile" : "desktop";
  }
  function planProblem(plan) {
    if (!plan || typeof plan !== "object" || Array.isArray(plan)) return "Random assignment must be an object.";
    if (!/^[a-z][a-z0-9_]*$/.test(plan.id || "")) return "Random assignment needs a stable lowercase ID.";
    if (Object.keys(plan).some(k=>!["id","method","unit","conditions","block_size","assignment_point","persistence_key","source_file","store"].includes(k))) return "Random assignment contains unsupported settings.";
    if (!["simple", "fixed_block"].includes(plan.method)) return "Choose simple or fixed_block random assignment.";
    if (plan.unit !== "respondent" || plan.persistence_key !== "session_id") return "Random assignment currently requires respondent units and session_id persistence.";
    const weights = plan.conditions, values = Object.values(weights || {}), total = values.reduce((a,b) => a+b, 0);
    if (!weights || typeof weights !== "object" || Array.isArray(weights) || values.length < 2 || values.some(w => !Number.isSafeInteger(w) || w < 1) || total > 1000) return "Condition weights must be positive integers with a total no greater than 1000.";
    if (Object.keys(weights).some(k=>!/^[a-z][a-z0-9_]*$/.test(k))) return "Condition IDs must use lowercase letters, digits, and underscores.";
    if (plan.method === "fixed_block") {
      if (!Number.isSafeInteger(plan.block_size) || plan.block_size < 2 || plan.block_size > 1000 || plan.block_size % total) return "Block size must be a multiple of the total condition weights, between 2 and 1000.";
    } else if ("block_size" in plan) return "Simple random assignment must not specify block_size.";
    return null;
  }
  function randomBelow(n) {
    if (!Number.isSafeInteger(n) || n < 1 || n > 4294967296) throw new Error("Invalid random bound");
    const limit = Math.floor(4294967296 / n) * n, bytes = new Uint32Array(1);
    do { globalThis.crypto.getRandomValues(bytes); } while (bytes[0] >= limit);
    return bytes[0] % n;
  }
  function shuffle(items, randbelow = randomBelow) {
    const result = [...items];
    for (let i=result.length-1; i>0; i--) { const j=randbelow(i+1); [result[i],result[j]]=[result[j],result[i]]; }
    return result;
  }
  function drawAssignment(plan, sequence, randbelow = randomBelow) {
    const problem = planProblem(plan); if (problem) throw new Error(problem);
    const entries=Object.entries(plan.conditions).sort(([a],[b])=>a<b?-1:a>b?1:0), total=entries.reduce((n,[,w])=>n+w,0);
    if (plan.method === "simple") {
      let n=randbelow(total);
      for (const [condition,w] of entries) { n-=w; if (n<0) return {condition,block_id:null}; }
    }
    if (!sequence.remaining?.length) {
      sequence.remaining=shuffle(entries.flatMap(([c,w])=>Array(w*plan.block_size/total).fill(c)),randbelow);
      sequence.block=(sequence.block || 0)+1;
    }
    return {condition:sequence.remaining.shift(),block_id:String(sequence.block)};
  }
  function questionOrder(page, randbelow=randomBelow) {
    const selected=page.shuffle_questions || [], shuffled=shuffle(selected,randbelow);
    return (page.questions || []).map(q=>selected.includes(q.id)?shuffled.shift():q.id);
  }
  function optionPlan(parsed) {
    const settings=parsed.front_matter?.["survey-settings"] || {}, questions=new Map(parsed.pages.flatMap(p=>p.questions).map(q=>[q.id,q])), types=new Set(["mc","mc_buttons","mc_multiple","mc_multiple_buttons","matrix"]), plans=new Map(), seen=new Set(), result=Object.create(null);
    if(typeof (settings["all-shuffled"] ?? false)!=="boolean") throw new Error("all-shuffled must be true or false.");
    if(settings["all-shuffled"]) for(const [id,q] of questions) if(types.has(q.type)) plans.set(id,null);
    if(!Array.isArray(settings.shuffled ?? [])) throw new Error("shuffled must be a list.");
    for(const entry of settings.shuffled || []) {
      let id,positions;
      if(typeof entry==="string") {id=entry;positions=null;}
      else if(entry && !Array.isArray(entry) && typeof entry==="object" && Object.keys(entry).length===1) [id,positions]=Object.entries(entry)[0];
      else throw new Error("Each shuffled entry must name one question.");
      if(seen.has(id)) throw new Error("Do not repeat a question in shuffled.");
      seen.add(id);
      if(!questions.has(id) || !types.has(questions.get(id).type)) throw new Error("shuffled supports mc, mc_buttons, mc_multiple, mc_multiple_buttons and matrix.");
      plans.set(id,positions);
    }
    for(const [id,positions] of plans) {
      const q=questions.get(id),items=q[q.type==="matrix"?"rows":"options"] || [], indices=positions==null?items.map((_,i)=>i+1):[];
      for(const part of positions==null?[]:Array.isArray(positions)?positions:[positions]) {
        if(Number.isInteger(part)) indices.push(part);
        else if(typeof part==="string" && /^[1-9]\d*-[1-9]\d*$/.test(part)) {
          const [a,b]=part.split("-").map(Number);
          if(a>b || b>items.length) throw new Error("Shuffle positions must be inside the question and ascending.");
          for(let i=a;i<=b;i++) indices.push(i);
        } else throw new Error("Use positive positions or ascending ranges for shuffled.");
      }
      if(!indices.length || new Set(indices).size!==indices.length || indices.some(i=>i<1 || i>items.length)) throw new Error("Shuffle positions must be distinct and inside the question.");
      result[id]=indices.map(i=>items[i-1].value);
    }
    return result;
  }
  function optionOrder(q, randbelow=randomBelow) {
    const items=q[q.type==="matrix"?"rows":"options"] || [], selected=q.shuffle_items || [], randomized=shuffle(selected,randbelow);
    return items.map(o=>selected.includes(o.value)?randomized.shift():o.value);
  }
  function pagePlan(parsed,config) {
    const selected=config.page_order ?? [];
    if(!Array.isArray(selected) || selected.some(p=>typeof p!=="string")) throw new Error("page_order must be a list of page IDs.");
    if(!selected.length) return [];
    const pages=parsed.pages,ids=pages.map(p=>p.id);
    if((parsed.front_matter?.["survey-settings"]?.["start-page"] ?? ids[0])!==ids[0])throw new Error("Page shuffling must start at the fixed opening page.");
    if(selected.length<2 || new Set(selected).size!==selected.length || selected.some(p=>!ids.includes(p))) throw new Error("Choose at least two distinct existing pages for page_order.");
    const positions=selected.map(p=>ids.indexOf(p)).sort((a,b)=>a-b);
    if(positions.some((p,i)=>p!==positions[0]+i) || positions[0]===0 || positions.at(-1)===ids.length-1) throw new Error("Shuffle one contiguous group between fixed opening and ending pages.");
    const protectedPages=new Set(Object.values(config.outcomes || {}).map(o=>o.page));
    for(const p of pages) if(p.questions.some(q=>q.id===config.consent?.confirmation_question)) protectedPages.add(p.id);
    for(const r of config.randomization || []) {protectedPages.add(r.assignment_point?.after_page);for(const p of r.assignment_point?.before_condition_pages || []) protectedPages.add(p);}
    if(selected.some(p=>protectedPages.has(p))) throw new Error("Keep consent, assignment, condition and ending pages fixed.");
    if(pages.some(p=>selected.includes(p.id) && p.nav?.page_next)) throw new Error("Shuffled pages must use automatic next-page navigation.");
    if(config.logic?.skip?.length || config.logic?.show?.length) throw new Error("Page shuffling currently requires an independent linear survey without skip/show rules.");
    if(pages.some(p=>p.nav?.page_next)) throw new Error("Remove explicit incoming links to shuffled pages.");
    return ids.filter(p=>selected.includes(p));
  }
  function pageOrder(model,randbelow=randomBelow) {
    const selected=model.shuffle_pages || [], randomized=shuffle(selected,randbelow);
    return model.pages.map(p=>selected.includes(p.id)?randomized.shift():p.id);
  }
  function redirectPlan(outcome) {
    if(!outcome.redirect)return null;
    if(typeof outcome.redirect!=="string")throw new Error("Redirect must be a fixed HTTPS URL.");
    let url;try{url=new URL(outcome.redirect);}catch{throw new Error("Redirect must be a fixed HTTPS URL without credentials.");}
    if(url.protocol!=="https:" || !url.hostname || url.username || url.password || /[\s\\<>]/.test(outcome.redirect))throw new Error("Redirect must be a fixed HTTPS URL without credentials.");
    const params=outcome.redirect_params ?? {},delay=outcome.redirect_delay ?? null,newtab=outcome.redirect_newtab ?? false;
    if(!params || typeof params!=="object" || Array.isArray(params) || Object.entries(params).some(([k,v])=>typeof v!=="string" || !/^[A-Za-z][A-Za-z0-9_]{0,63}$/.test(k) || !/^[A-Za-z][A-Za-z0-9_]{0,63}$/.test(v)))throw new Error("Redirect parameters must map approved output names to input URL parameter names.");
    if([...Object.keys(params),...Object.values(params)].some(v=>v==='gq_preview' || /token|secret|password|key/i.test(v)))throw new Error("Do not forward credentials in redirect parameters.");
    if(Object.keys(params).length && (url.hash || Object.keys(params).some(k=>url.searchParams.has(k))))throw new Error("Dynamic redirects must not have a fragment or duplicate fixed query keys.");
    if(delay!==null && (!Number.isInteger(delay) || delay<0 || delay>3600))throw new Error("Redirect delay must be an integer from 0 to 3600 seconds.");
    if(typeof newtab!=="boolean")throw new Error("redirect_newtab must be true or false.");
    if(newtab && delay!==null)throw new Error("New-tab redirects require a click, not an automatic timer.");
    return {url:outcome.redirect,params,delay,newtab,label:String(outcome.redirect_label ?? "Continue to the next website")};
  }
  function redirectUrl(plan,query) {
    const url=new URL(plan.url),input=new URLSearchParams(query);
    for(const [key,source] of Object.entries(plan.params)) {
      const values=input.getAll(source);
      if(values.length!==1 || !values[0])throw new Error("Required return-link parameter is missing or repeated.");
      url.searchParams.set(key,values[0]);
    }
    return url.href;
  }
  function orderingProblems(parsed, config) {
    const problems=[],seen=new Set(),rules=Object.hasOwn(config,"question_order") ? config.question_order : [];
    if (!Array.isArray(rules)) return ["question_order must be a list of page/question groups."];
    for(const rule of rules) {
      if (!rule || typeof rule!=="object" || Array.isArray(rule)) {problems.push("Each question_order entry must identify a page and questions.");continue;}
      const page=parsed.pages.find(p=>p.id===rule.page),selected=rule.questions;
      if (Object.keys(rule).some(k=>!["page","questions"].includes(k))) problems.push("Question shuffling contains unsupported settings.");
      if (!page || seen.has(rule.page)) {problems.push("Question shuffling requires one group per existing page.");continue;}
      seen.add(rule.page); const ids=page.questions.map(q=>q.id);
      if (!Array.isArray(selected) || selected.length<2 || selected.some(q=>typeof q!=="string" || !ids.includes(q)) || new Set(selected).size!==selected.length) {problems.push("Choose at least two distinct questions on the same page to shuffle.");continue;}
      if (ids.includes(config.consent?.confirmation_question)) problems.push("Keep the consent page in its approved fixed order.");
      for (const show of config.logic?.show || []) {
        const refs=String(show.if || "").match(/[a-z][a-z0-9_]*/g) || [];
        if (ids.includes(show.question) && refs.some(r=>ids.includes(r)) && (selected.includes(show.question) || refs.some(r=>selected.includes(r)))) problems.push("Keep dependent questions and their same-page trigger questions outside shuffled groups.");
      }
    }
    return problems;
  }
  function boundaryProblems(parsed, config) {
    const ids=parsed.pages.map(p=>p.id),problems=[],consent=config.consent?.confirmation_question;
    const consentPage=parsed.pages.find(p=>p.questions.some(q=>q.id===consent))?.id;
    for(const plan of config.randomization || []) {
      const after=plan.assignment_point?.after_page;
      if(!ids.includes(after))continue;
      if(consentPage && ids.indexOf(after)<ids.indexOf(consentPage))problems.push("Place random assignment after consent, not before it.");
      const targets=plan.assignment_point?.before_condition_pages || [];
      if(!Array.isArray(targets) || !targets.length || targets.some(t=>!ids.includes(t) || ids.indexOf(t)<=ids.indexOf(after)))problems.push("List the condition pages after the assignment boundary.");
    }
    return problems;
  }
  function allocate(allocations, sequences, id, conditions, plan, scope="preview") {
    if (!plan) {
      if (conditions.length===1) return conditions[0];
      throw new Error("An explicit random assignment plan is required.");
    }
    const key=JSON.stringify([scope,plan.id]), signature=JSON.stringify(plan);
    const sequence=sequences[key] ||= {signature};
    if (sequence.signature!==signature) throw new Error("The random assignment plan changed; create a new study ID.");
    const existing=allocations.find(a=>a.id===id && a.scope===key);
    if (existing) return existing.condition;
    const result=drawAssignment(plan,sequence);
    allocations.push({id,scope:key,randomization_id:plan.id,method:plan.method,...result,draw_id:globalThis.crypto.randomUUID(),assigned_at:new Date().toISOString()});
    return result.condition;
  }
  function withdrawnState(state) {
    return {page:state.page,lifecycle:'withdrawn',answers:{},history:[],visited:[state.page],condition:null,consent_accepted:false,question_orders:{},option_orders:{},...('_revision' in state?{_revision:state._revision}:{})};
  }
  function createMemoryBackend(saved = {}) {
    const sessions = new Map(),
      allocations = saved.allocations || [], sequences = saved.sequences || {};
    return {
      kind: "memory",
      load: (id) => sessions.get(id) || null,
      save: (id, state) => sessions.set(id, JSON.parse(JSON.stringify(state.lifecycle==='withdrawn'?withdrawnState(state):state))),
      clear: (id) => sessions.delete(id),
      assign: (id, conditions, plan, scope) => allocate(allocations,sequences,id,conditions,plan,scope),
      inspect: () => ({
        sessions: [...sessions.entries()],
        allocations: [...allocations],
        sequences,
      }),
    };
  }
  function createLocalMockBackend(namespace = "greedyq-mock") {
    const memory = createMemoryBackend(),
      key = `${namespace}:state`;
    try {
      const saved = JSON.parse(localStorage.getItem(key) || "null");
      for (const [id, state] of saved?.sessions || []) memory.save(id, state);
      for (const item of saved?.allocations || [])
        memory.assign(item.id, [item.condition]);
    } catch {}
    const persist = () => {
      try {
        localStorage.setItem(key, JSON.stringify(memory.inspect()));
      } catch {}
    };
    return {
      kind: "local-mock",
      load: memory.load,
      save: (id, s) => {
        memory.save(id, s);
        persist();
      },
      clear: (id) => {
        memory.clear(id);
        persist();
      },
      assign: (id, c) => {
        const value = memory.assign(id, c);
        persist();
        return value;
      },
      inspect: memory.inspect,
    };
  }
  function createConcurrentLocalMockBackend(namespace = "greedyq-mock") {
    // file: origins do not provide portable cross-tab storage/lock semantics.
    // Each file preview tab therefore owns its simulation; refresh still resumes it.
    const fileMode=globalThis.location?.protocol === "file:",
      storage=fileMode ? sessionStorage : localStorage,
      key = `${namespace}:state:randomization1`,
      empty = () => ({ sessions: [], allocations: [], sequences: {} }),
      read = () => {
        if (activeData) return activeData;
        if (shared) return cache;
        try {
          return JSON.parse(storage.getItem(key) || "null") || empty();
        } catch {
          return empty();
        }
      },
      write = (data) => { if (shared) {activeData=data;return;} storage.setItem(key, JSON.stringify(data)); },
      clone = (value) =>
        value == null ? null : JSON.parse(JSON.stringify(value));
    const shared=!fileMode && typeof window!=="undefined";
    let activeData=null,cache=empty();
    const opened=shared ? new Promise((resolve,reject)=>{
      const request=indexedDB.open("greedyq-preview-randomization1",1);
      request.onupgradeneeded=()=>request.result.createObjectStore("states");
      request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error);
    }) : null;
    const transaction=run=>opened.then(db=>new Promise((resolve,reject)=>{
      const tx=db.transaction("states","readwrite"),store=tx.objectStore("states"),request=store.get(key);
      let result,data;
      request.onsuccess=()=>{
        try {activeData=request.result || empty();result=run();data=activeData;store.put(data,key);activeData=null;}
        catch(error){activeData=null;tx.abort();reject(error);}
      };
      tx.oncomplete=()=>{cache=data;resolve(result);};
      tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error || new Error("Preview transaction aborted"));
    }));
    const ready=shared ? transaction(()=>null) : Promise.resolve();
    const locked=run=>shared ? ready.then(()=>transaction(run)) : run();
    return {
      kind: "local-mock",
      ready,
      synchronize:()=>locked(()=>clone(read())),
      load(id) {
        const found = read().sessions.find((item) => item[0] === id);
        return found ? clone(found[1]) : null;
      },
      save(id, state) {
        const snapshot=clone(state);
        return locked(()=>{
        const data = read(),
          index = data.sessions.findIndex((item) => item[0] === id),
          current = index < 0 ? null : data.sessions[index][1],
          expected = Number(state._revision || 0);
        if (current && Number(current._revision || 0) !== expected)
          return { status: "conflict", current: clone(current) };
        const saved = snapshot.lifecycle==='withdrawn'?withdrawnState(snapshot):snapshot;
        saved._revision = expected + 1;
        state._revision = saved._revision;
        if (index < 0) data.sessions.push([id, saved]);
        else data.sessions[index] = [id, saved];
        write(data);
        return { status: "saved", revision: saved._revision };
        });
      },
      clear(id) {
        return locked(()=>{
        const data = read();
        data.sessions = data.sessions.filter((item) => item[0] !== id);
        // Consumed slots must not be reused after withdrawal.
        write(data);
        return { status: "deleted" };
        });
      },
      assign(id, conditions, plan, scope) {
        const run=()=>{const data = read();
          const condition=allocate(data.allocations,data.sequences ||= {},id,conditions,plan,scope);
          write(data); return condition;};
        return locked(run);
      },
      inspect: read,
    };
  }
  function createSupabaseBackend({ url, anonKey }) {
    if (!/^https:\/\//.test(url || "") || !anonKey)
      throw new Error("Supabase URL and anonymous key are required.");
    const rpc = async (name, body) => {
      const response = await fetch(
        `${url.replace(/\/$/, "")}/rest/v1/rpc/${name}`,
        {
          method: "POST",
          headers: {
            apikey: anonKey,
            Authorization: `Bearer ${anonKey}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        },
      );
      if (!response.ok)
        throw new Error(`Supabase RPC ${name} failed (${response.status}).`);
      return response.status === 204 ? null : response.json();
    };
    return {
      kind: "supabase",
      load: (id) => rpc("greedyq_resume_session", { p_session_id: id }),
      save: (id, state) =>
        rpc("greedyq_save_session", { p_session_id: id, p_state: state }),
      clear: (id) => rpc("greedyq_withdraw_session", { p_session_id: id }),
      assign: (id, conditions) =>
        rpc("greedyq_assign_condition", {
          p_session_id: id,
          p_conditions: conditions,
        }),
    };
  }
  function createSecureSupabaseBackend({
    url,
    anonKey,
    accessToken,
    studyId,
    studyVersion = "unknown",
    greedyqVersion,
    specVersion = "0.2",
    isTest = true,
    consentQuestion = null,
  }) {
    if (!accessToken || accessToken.length < 24)
      throw new Error("A strong session access token is required.");
    const base = createSupabaseBackend({ url, anonKey }),
      call = async (name, body) => {
        const response = await fetch(
          `${url.replace(/\/$/, "")}/rest/v1/rpc/${name}`,
          {
            method: "POST",
            headers: {
              apikey: anonKey,
              Authorization: `Bearer ${anonKey}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
          },
        );
        if (!response.ok) {
          const detail=await response.json().catch(()=>({}));
          const error=new Error(`Supabase RPC ${name} failed (${response.status}).`);
          if(detail.message==='This study is closed for archiving')error.kind='study_closed';
          if(name==='greedyq_start_prolific' && /duplicate Prolific/.test(detail.message || ''))error.kind='prolific_duplicate';
          throw error;
        }
        return response.status === 204 ? null : response.json();
      };
    return {
      kind: "supabase-secure",
      create: (id) =>
        call("greedyq_create_session", {
          p_session_id: id,
          p_access_token: accessToken,
          p_study_id: studyId,
          p_study_version: studyVersion,
          p_spec_version: specVersion,
          p_greedyq_version: greedyqVersion,
          p_is_test: isTest,
        }),
      load: (id) =>
        call("greedyq_resume_session", {
          p_session_id: id,
          p_access_token: accessToken,
        }),
      save: (id, state) =>
        call("greedyq_save_session", {
          p_session_id: id,
          p_access_token: accessToken,
          p_state: state,
          p_consent_question: consentQuestion,
        }),
      clear: (id) =>
        call("greedyq_withdraw_session", {
          p_session_id: id,
          p_access_token: accessToken,
        }),
      assign: (id, conditions) =>
        call("greedyq_assign_condition", {
          p_session_id: id,
          p_access_token: accessToken,
          p_study_id: studyId,
          p_study_version: studyVersion,
          p_spec_version: specVersion,
          p_greedyq_version: greedyqVersion,
          p_conditions: conditions,
          p_is_test: isTest,
        }),
      registerExternal: (id, identifiers) =>
        call("greedyq_register_external", {
          p_session_id: id,
          p_access_token: accessToken,
          p_provider: "prolific",
          p_participant_id: identifiers.PROLIFIC_PID,
          p_external_study_id: identifiers.STUDY_ID,
          p_external_session_id: identifiers.SESSION_ID,
        }),
      startProlific:(id,identifiers,previewToken)=>call(previewToken?'greedyq_start_prolific_preview':'greedyq_start_prolific',{
        p_session_id:id,p_access_token:accessToken,p_study_id:studyId,p_study_version:studyVersion,p_spec_version:specVersion,p_greedyq_version:greedyqVersion,p_is_test:isTest,
        p_participant_id:identifiers.PROLIFIC_PID,p_external_study_id:identifiers.STUDY_ID,p_external_session_id:identifiers.SESSION_ID,
        ...(previewToken?{p_preview_token:previewToken}:{})
      }),
      raw: base,
    };
  }
  function prolificPlan(config) {
    const r=config.respondents || {};if(r.source!=='prolific')return null;
    const mode=r.mode || 'test',s=r.prolific || {},paths={},codes=[];
    if(typeof s!=='object' || Array.isArray(s))throw new Error('respondents.prolific must be an object.');
    if(Object.keys(s).some(k=>!['study_id','completion_paths_reviewed','screening_mode'].includes(k)))throw new Error('Unsupported Prolific setting; use the standard URL integration.');
    const id=s.study_id ?? null;
    if(id!==null && !/^[a-fA-F0-9]{24}$/.test(String(id)))throw new Error('Set respondents.prolific.study_id to the 24-character Prolific study ID.');
    if(mode==='production' && !id)throw new Error('Set respondents.prolific.study_id before Prolific production collection.');
    if(!['resume','block'].includes(r.duplicate_policy || 'resume'))throw new Error('Prolific duplicate policy must be resume or block; repeated submissions are not enabled.');
    const screening=s.screening_mode || 'none';
    if(!['none','prescreener_validation','custom'].includes(screening))throw new Error('Choose none, prescreener_validation or custom for Prolific screening_mode.');
    if('completion_paths_reviewed' in s && typeof s.completion_paths_reviewed!=='boolean')throw new Error('completion_paths_reviewed must record a boolean researcher review.');
    if(mode==='production' && !s.completion_paths_reviewed)throw new Error('Review Prolific completion paths before production collection.');
    for(const [key,outcome] of Object.entries(config.outcomes || {})) {
      if(!outcome.redirect){if(mode==='production')throw new Error('Each Prolific outcome needs its own configured completion path: '+key);continue;}
      let u;try{u=new URL(outcome.redirect);}catch{throw new Error('Use the exact Prolific HTTPS completion URL with a single cc parameter: '+key);}
      if(u.protocol!=='https:' || !['app.prolific.com','app.prolific.co'].includes(u.host) || u.username || u.password || u.pathname!=='/submissions/complete' || u.hash || [...u.searchParams.keys()].some(k=>k!=='cc') || u.searchParams.getAll('cc').length!==1)throw new Error('Use the exact Prolific HTTPS completion URL with a single cc parameter: '+key);
      const code=u.searchParams.get('cc');
      if(!/^[A-Za-z0-9_-]{2,100}$/.test(code))throw new Error('Invalid Prolific completion code: '+key);
      if(mode==='production' && (!/^[A-Za-z0-9]{2,100}$/.test(code) || /EXAMPLE|PLACEHOLDER|TEST/i.test(code)))throw new Error('Replace fixture completion codes with codes from your Prolific study: '+key);
      if(codes.includes(code))throw new Error('Use distinct Prolific codes for distinct outcomes.');
      codes.push(code);paths[key]={page:outcome.page || key,status:outcome.lifecycle_state || key,url:outcome.redirect,code};
    }
    if(mode==='production' && !Object.values(paths).some(p=>p.status==='completed'))throw new Error('A Prolific completion path is required before production collection.');
    if(mode==='production' && screening==='none' && Object.values(paths).some(p=>p.status==='screened_out'))throw new Error('Review Prolific screening_mode before using a screen-out path.');
    return {study_id:id,identity_verification:'url_parameters_only',screening_mode:screening,completion_paths_reviewed:s.completion_paths_reviewed || false,paths};
  }
  function parseProlificLaunch(search, mode = "test", expectedStudyId=null) {
    const raw=String(search),params = new URLSearchParams(raw.includes('://')?new URL(raw).search:raw.replace(/^\?/, "")),
      identifiers = Object.fromEntries(
        ["PROLIFIC_PID", "STUDY_ID", "SESSION_ID"].map((key) => [
          key,
          params.get(key),
        ]),
      ),
      issues = [];
    for (const [key, value] of Object.entries(identifiers)) {
      if (!value)
        issues.push({
          code: "GQ020",
          message: `${key} is required for a Prolific launch.`,
        });
      else if (value.length > 200)
        issues.push({ code: "GQ020", message: `${key} is too long.` });
      else if(!/^[A-Za-z0-9_-]+$/.test(value))issues.push({code:'GQ020',message:`${key} contains invalid characters.`});
      else if(mode==='production' && !/^[a-fA-F0-9]{24}$/.test(value))issues.push({code:'GQ020',message:`${key} must be a 24-character Prolific ID in production.`});
      if(params.getAll(key).length>1)issues.push({code:'GQ020',message:`${key} must occur exactly once.`});
    }
    if(expectedStudyId && identifiers.STUDY_ID!==expectedStudyId)issues.push({code:'GQ020',message:'The Prolific study ID does not match this survey.'});
    if(params.has('prolific_token'))issues.push({code:'GQ020',message:'Signed Prolific launches require server-side verification, which is not enabled.'});
    if(params.has('gq_preview') && (mode!=='test' || params.getAll('gq_preview').length!==1 || !/^[a-f0-9]{64}$/.test(params.get('gq_preview') || '')))issues.push({code:'GQ020',message:'A repeat preview requires one valid test-only grant.'});
    if (!["test", "production"].includes(mode))
      issues.push({
        code: "GQ020",
        message: "Respondent mode must be test or production.",
      });
    return {
      status: issues.length ? "failed" : "passed",
      mode,
      identifiers,
      issues,
    };
  }
  function resolveProlificLaunch(search, mode = "test", expectedStudyId=null) {
    const parsed = parseProlificLaunch(search, mode, expectedStudyId),
      raw=String(search),params=new URLSearchParams(raw.includes('://')?new URL(raw).search:raw.replace(/^\?/,'')),supplied=['PROLIFIC_PID','STUDY_ID','SESSION_ID','prolific_token','gq_preview'].filter(k=>params.has(k));
    if (parsed.status === "passed") return { ...parsed, source: "prolific" };
    if (mode === "test" && supplied.length === 0)
      return { status: "passed", mode, source: "direct_test", identifiers: null, issues: [] };
    return { ...parsed, source: "invalid" };
  }
  function stableSessionId(studyId, provided) {
    const key = `greedyq-session:${studyId}`;
    if (
      provided &&
      /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(
        provided,
      )
    ) {
      localStorage.setItem(key, provided);
      return provided;
    }
    const prior = localStorage.getItem(key);
    if (prior) return prior;
    const created = crypto.randomUUID();
    localStorage.setItem(key, created);
    return created;
  }
  const esc = (v) =>
    String(v ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  function inlineMarkdown(value) {
    let text=esc(String(value ?? '').replaceAll('\x00','\ufffd'));const tokens=[];
    text=text.replace(/`([^`\n]+)`/g,(_,content)=>{tokens.push('<code>'+content+'</code>');return '\x00'+(tokens.length-1)+'\x00';});
    text=text.replace(/\*\*\*([^*\n]+)\*\*\*/g,'<strong><em>$1</em></strong>').replace(/\*\*([^*\n]+)\*\*/g,'<strong>$1</strong>').replace(/\*([^*\n]+)\*/g,'<em>$1</em>');
    return text.replace(/\x00(\d+)\x00/g,(_,index)=>tokens[Number(index)]);
  }
  function mountRespondent(root, model, options = {}) {
    const t=(message,values)=>translate(model.language || 'en',message,values);
    root.lang=model.language || 'en';
    const mode = options.mode || detectDevice(root.ownerDocument.defaultView),
      backend = options.backend || createMemoryBackend(),
      sessionId =
        options.sessionId || `virtual-${Math.random().toString(36).slice(2)}`,
      pages = new Map(model.pages.map((p) => [p.id, p])),
      fresh = () => ({
        page: model.start_page,
        history: [],
        answers: {},
        question_orders: {},
        condition: model.assignment_page ? null : "default",
        lifecycle: "active",
        visited: [],
      }),
      state = backend.load(sessionId) || fresh();
    if(model.shuffle_pages) {
      state.page_order ||= pageOrder(model);
      const expected=model.pages.map(p=>p.id), actual=state.page_order;
      if(actual.length!==expected.length || new Set(actual).size!==expected.length || actual.some(p=>!expected.includes(p)) || expected.some((p,i)=>!model.shuffle_pages.includes(p) && actual[i]!==p)) throw new Error("Page order changed; start a new study version/session.");
    }
    root.className = `gq-app gq-${mode}`;
    root.innerHTML = `<div class="gq-top"><b>${esc(model.organization || t("Research team"))}</b><span class="gq-progress"></span></div><main class="gq-card" aria-live="polite"></main>`;
    const card = root.querySelector(".gq-card"),
      progress = root.querySelector(".gq-progress");
    const value = (f) =>
        f === "condition" ? state.condition : state.answers[f],
      matches = (r) => matchesCondition(r,state.answers,state.condition),
      visible = (p) => {
        const byId=new Map((p.questions || []).map(q=>[q.id,q]));
        state.question_orders ||= {};
        const ids=Object.hasOwn(state.question_orders,p.id) ? state.question_orders[p.id] : (state.question_orders[p.id]=questionOrder(p));
        if (ids.length!==byId.size || new Set(ids).size!==byId.size || ids.some(id=>!byId.has(id))) throw new Error("Question order changed; start a new study version/session.");
        return ids.map(id=>byId.get(id)).filter(q=>matches(q.show_if)).map(q=>{
          if(!q.shuffle_items) return q;
          state.option_orders ||= {};
          const collection=q.type==="matrix"?"rows":"options", items=q[collection], order=Object.hasOwn(state.option_orders,q.id)?state.option_orders[q.id]:(state.option_orders[q.id]=optionOrder(q));
          if(order.length!==items.length || new Set(order).size!==items.length || order.some(v=>!items.some(o=>o.value===v)) || items.some((o,i)=>!q.shuffle_items.includes(o.value) && order[i]!==o.value)) throw new Error("Option order changed; start a new study version/session.");
          return {...q,[collection]:order.map(v=>items.find(o=>o.value===v))};
        });
      },
      nextFor = (p) => {
        const following=x=>(x.routes || []).find(r=>matches(r.when))?.to ?? (state.page_order ? state.page_order[state.page_order.indexOf(x.id)+1] : x.next);
        let target=following(p);const seen=new Set([p.id]);
        while(pages.has(target) && !matches(pages.get(target).show_if)) {
          if(seen.has(target))return null;seen.add(target);target=following(pages.get(target));
        }
        return target;
      };
    function input(q) {
      const selected = state.answers[q.id] ?? q._answer,
        initial = selected ?? q.selected,
        today = new Date().toISOString().slice(0, 10);
      if (q.type === "custom")
        return `<div class="gq-custom ${esc(q.custom_class || "")}" data-customization="${esc(q.customization || "")}">${input({ ...q, type: q.base_type })}</div>`;
      if (q.type === "rank_order")
        return `<div class="gq-rank-order">${(q.options || []).map((o) => `<label><span>${inlineMarkdown(o.label)}</span><select data-rank-item="${esc(o.value)}"><option value="">${esc(t('Rank'))}</option>${q.options.map((_, i) => `<option value="${i + 1}" ${selected?.[o.value] === i + 1 ? "selected" : ""}>${i + 1}</option>`).join("")}</select></label>`).join("")}</div>`;
      if (q.type === "nps") {
        const min = q.min ?? 0, max = q.max ?? 10;
        return `<div class="gq-nps"><div class="gq-nps-scale">${Array.from({ length: max - min + 1 }, (_, i) => min + i).map((n) => `<label><input type="radio" name="${esc(q.id)}" value="${n}" ${selected === n ? "checked" : ""}><span>${n}</span></label>`).join("")}</div><div class="gq-nps-anchors"><span>${esc(q.low_label || t("Not at all likely"))}</span><span>${esc(q.high_label || t("Extremely likely"))}</span></div></div>`;
      }
      if (q.type === "timing")
        return `<input type="hidden" data-id="${esc(q.id)}" data-timing value="${Math.max(0, Math.round((Date.now() - (state.page_entered_at || Date.now())) / 1000))}">`;
      if (q.type === "constant_sum") {
        const total = q.total ?? 100;
        return `<div class="gq-constant-sum">${(q.options || []).map((o) => `<label><span>${inlineMarkdown(o.label)}</span><input type="number" min="0" step="${esc(q.step ?? 1)}" data-constant-item="${esc(o.value)}" value="${esc(selected?.[o.value] ?? 0)}"></label>`).join("")}<output data-constant-total>0 / ${esc(total)}</output></div>`;
      }
      if (q.type === "side_by_side")
        return `<div class="gq-side-by-side">${(q.columns || []).map((column) => `<section><h3>${esc(column.label)}</h3>${input({ ...q, id: `${q.id}:${column.value}`, type: "matrix", columns: undefined, mobile_columns: q.mobile_columns ?? 3, _answer: selected?.[column.value] })}</section>`).join("")}</div>`;
      if (q.type === "pick_group_rank")
        return `<div class="gq-pick-group-rank">${(q.options || []).map((o) => `<div class="gq-pgr-item"><strong>${esc(o.label)}</strong><label>${esc(t('Group'))}<select data-pgr-group="${esc(o.value)}"><option value="">${esc(t('Choose'))}</option>${(q.groups || []).map((g) => `<option value="${esc(g.value)}" ${selected?.[o.value]?.group === g.value ? "selected" : ""}>${esc(g.label)}</option>`).join("")}</select></label><label>${esc(t('Rank'))}<input type="number" min="1" max="${q.options.length}" data-pgr-rank="${esc(o.value)}" value="${esc(selected?.[o.value]?.rank ?? "")}"></label></div>`).join("")}</div>`;
      if (q.type === "drill_down") {
        const separator = q.path_separator || " > ", paths = (q.options || []).map((o) => String(o.label).split(separator)), current = Array.isArray(selected) ? selected : [], levels = Math.max(0, ...paths.map((p) => p.length));
        return `<div class="gq-drill-down" data-separator="${esc(separator)}">${Array.from({ length: levels }, (_, level) => { const prefix = current.slice(0, level); const choices = [...new Set(paths.filter((path) => prefix.every((part, i) => path[i] === part)).map((path) => path[level]).filter(Boolean))]; return `<label>${esc(t('Level'))} ${level + 1}<select data-drill-level="${level}"><option value="">${esc(t('Choose'))}</option>${choices.map((choice) => `<option value="${esc(choice)}" ${current[level] === choice ? "selected" : ""}>${esc(choice)}</option>`).join("")}</select></label>`; }).join("")}</div>`;
      }
      if (["mc", "mc_buttons", "mc_image"].includes(q.type))
        return (q.options || [])
          .map(
            (o, index) =>
              `<label class="gq-choice${q.type === "mc_buttons" ? " gq-button-choice" : ""}${q.type === "mc_image" ? " gq-image-choice" : ""}"><input type="radio" name="${esc(q.id)}" value="${esc(o.value)}" ${initial === o.value ? "checked" : ""}>${q.type === "mc_image" ? `<img src="${esc(q.images?.[index] || "")}" alt="${esc(o.label || t("Option") + " " + (index + 1))}">` : ""}${q.type !== "mc_image" || o.caption !== false ? `<span>${inlineMarkdown(o.label)}</span>` : ""}</label>`,
          )
          .join("");
      if (q.type === "slider") {
        const options = q.options || [],
          found = options.findIndex((option) => option.value === initial),
          index =
            found >= 0
              ? found
              : options.some((option) => option.value === q.selected)
                ? options.findIndex((option) => option.value === q.selected)
                : Math.floor(Math.max(0, options.length - 1) / 2),
          orientation = q.orientation || "horizontal",
          inputId = `${q.id}-slider`,
          outputId = `${q.id}-slider-output`;
        return `<div class="gq-slider gq-slider-${esc(orientation)}"><output id="${esc(outputId)}" for="${esc(inputId)}" aria-live="polite" data-slider-output="${esc(q.id)}">${esc(initial != null ? options[index]?.label || "" : t("Move the slider to answer."))}</output><input id="${esc(inputId)}" aria-label="${esc(q.label)}" aria-describedby="${esc(outputId)}" data-id="${esc(q.id)}" data-slider-kind="categorical" data-answer-initialized="${initial != null}" type="range" min="0" max="${Math.max(0, options.length - 1)}" step="1" value="${index}"><div class="gq-slider-labels"><span>${esc(options[0]?.label || "")}</span><span>${esc(options.at(-1)?.label || "")}</span></div></div>`;
      }
      if (q.type === "slider_numeric") {
        const values = (q.options || []).map((option) => Number(option.value)),
          min = q.min ?? (values.length ? Math.min(...values) : 0),
          max = q.max ?? (values.length ? Math.max(...values) : 100),
          step =
            q.step ?? (values.length > 1 ? Math.abs(values[1] - values[0]) : 1),
          defaults = Array.isArray(q.default)
            ? q.default
            : q.default != null
              ? [q.default]
              : [],
          current = selected ?? defaults[0] ?? Math.round((min + max) / 2),
          orientation = q.orientation || "horizontal",
          inputId = `${q.id}-slider`,
          outputId = `${q.id}-slider-output`;
        if (defaults.length === 2 || Array.isArray(selected)) {
          const range = Array.isArray(selected) ? selected : defaults;
          return `<div class="gq-slider gq-slider-range"><output id="${esc(outputId)}" aria-live="polite" data-slider-output="${esc(q.id)}">${esc(range.join(q.sep || " – "))}</output><input aria-label="${esc(q.label)} ${esc(t('minimum'))}" aria-describedby="${esc(outputId)}" data-id="${esc(q.id)}" data-range-index="0" data-slider-kind="numeric-range" data-answer-initialized="${selected != null || defaults.length === 2}" type="range" min="${esc(min)}" max="${esc(max)}" step="${esc(step)}" value="${esc(range[0])}"><input aria-label="${esc(q.label)} ${esc(t('maximum'))}" aria-describedby="${esc(outputId)}" data-id="${esc(q.id)}" data-range-index="1" data-slider-kind="numeric-range" data-answer-initialized="${selected != null || defaults.length === 2}" type="range" min="${esc(min)}" max="${esc(max)}" step="${esc(step)}" value="${esc(range[1])}"><div class="gq-slider-labels"><span>${esc(min)}</span><span>${esc(max)}</span></div></div>`;
        }
        return `<div class="gq-slider gq-slider-${esc(orientation)}"><output id="${esc(outputId)}" for="${esc(inputId)}" aria-live="polite" data-slider-output="${esc(q.id)}">${esc(selected != null || defaults.length ? (q.pre || "") + current : t("Move the slider to answer."))}</output><input id="${esc(inputId)}" aria-label="${esc(q.label)}" aria-describedby="${esc(outputId)}" data-id="${esc(q.id)}" data-slider-kind="numeric" data-answer-initialized="${selected != null || defaults.length > 0}" type="range" min="${esc(min)}" max="${esc(max)}" step="${esc(step)}" value="${esc(current)}"><div class="gq-slider-labels"><span>${esc(min)}</span><span>${esc(max)}</span></div></div>`;
      }
      if (
        ["mc_multiple", "mc_multiple_buttons", "mc_multiple_image"].includes(
          q.type,
        )
      )
        return (q.options || [])
          .map(
            (o, index) =>
              `<label class="gq-choice${q.type === "mc_multiple_buttons" ? " gq-button-choice" : ""}${q.type === "mc_multiple_image" ? " gq-image-choice" : ""}"><input type="checkbox" name="${esc(q.id)}" value="${esc(o.value)}" ${Array.isArray(initial) && initial.includes(o.value) ? "checked" : ""}>${q.type === "mc_multiple_image" ? `<img src="${esc(q.images?.[index] || "")}" alt="${esc(o.label || t("Option") + " " + (index + 1))}">` : ""}${q.type !== "mc_multiple_image" || o.caption !== false ? `<span>${inlineMarkdown(o.label)}</span>` : ""}</label>`,
          )
          .join("");
      if (q.type === "select")
        return `<select data-id="${esc(q.id)}"><option value="">${esc(q.placeholder || t("Choose one"))}</option>${q.options.map((o) => `<option value="${esc(o.value)}" ${selected === o.value ? "selected" : ""}>${esc(o.label)}</option>`).join("")}</select>`;
      if (["audio", "video"].includes(q.type)) {
        const attributes = [
          q.controls !== false ? "controls" : "",
          q.autoplay ? "autoplay" : "",
          q.muted ? "muted" : "",
          q.loop ? "loop" : "",
          `preload="${esc(q.preload || "metadata")}"`,
        ]
          .filter(Boolean)
          .join(" ");
        const transcript = q.transcript
          ? `<details class="gq-transcript"><summary>${esc(t('Transcript'))}</summary><p>${esc(q.transcript)}</p></details>`
          : "";
        if (q.type === "audio")
          return `<figure class="gq-media"><audio aria-label="${esc(q.label)}" src="${esc(q.src)}" ${attributes}></audio>${q.caption ? `<figcaption>${esc(q.caption)}</figcaption>` : ""}${transcript}</figure>`;
        return `<figure class="gq-media"><video aria-label="${esc(q.label)}" src="${esc(q.src)}" ${q.poster ? `poster="${esc(q.poster)}"` : ""} ${attributes}></video>${q.caption ? `<figcaption>${esc(q.caption)}</figcaption>` : ""}${transcript}</figure>`;
      }
      if (["matrix", "matrix_multiple"].includes(q.type)) {
        const rawWidth = String(q.matrix_question_width ?? "40").replace(
            "%",
            "",
          ),
          numericWidth = Number(rawWidth),
          promptWidth =
            Number.isFinite(numericWidth) &&
            numericWidth > 0 &&
            numericWidth < 100
              ? numericWidth
              : 40,
          cellType = q.type === "matrix_multiple" ? "checkbox" : "radio";
        if (mode === "mobile") {
          const chunkSize = q.mobile_columns ?? 3,
            chunks = [];
          for (let index = 0; index < q.options.length; index += chunkSize)
            chunks.push(q.options.slice(index, index + chunkSize));
          return `<div class="gq-matrix-mobile" role="group" aria-label="${esc(q.label)}">${q.rows
            .map(
              (r) =>
                `<section class="gq-matrix-mobile-row"><h3>${esc(r.label)}</h3>${chunks
                  .map(
                    (chunk) =>
                      `<div class="gq-matrix-mobile-chunk" style="--gq-mobile-columns:${chunk.length}">${chunk
                        .map((o) => {
                          const checked =
                            q.type === "matrix_multiple"
                              ? Array.isArray(selected?.[r.value]) &&
                                selected[r.value].includes(o.value)
                              : selected?.[r.value] === o.value;
                          return `<label class="gq-matrix-mobile-cell"><span>${inlineMarkdown(o.label)}</span><input type="${cellType}" aria-label="${esc(`${r.label} — ${o.label}`)}" name="${esc(q.id + ":" + r.value)}" value="${esc(o.value)}" ${checked ? "checked" : ""}></label>`;
                        })
                        .join("")}</div>`,
                  )
                  .join("")}</section>`,
            )
            .join("")}</div>`;
        }
        return `<div class="gq-matrix" role="region" aria-label="${esc(q.label)}" tabindex="0"><table><colgroup><col style="width:${promptWidth}%">${q.options.map(() => `<col style="width:${(100 - promptWidth) / q.options.length}%">`).join("")}</colgroup><thead><tr><th class="gq-matrix-corner" scope="col"></th>${q.options.map((o) => `<th scope="col">${esc(o.label)}</th>`).join("")}</tr></thead><tbody>${q.rows
          .map(
            (r) =>
              `<tr><th scope="row">${esc(r.label)}</th>${q.options
                .map((o) => {
                  const checked =
                    q.type === "matrix_multiple"
                      ? Array.isArray(selected?.[r.value]) &&
                        selected[r.value].includes(o.value)
                      : selected?.[r.value] === o.value;
                  return `<td><label class="gq-matrix-cell"><input type="${cellType}" aria-label="${esc(`${r.label} — ${o.label}`)}" name="${esc(q.id + ":" + r.value)}" value="${esc(o.value)}" ${checked ? "checked" : ""}></label></td>`;
                })
                .join("")}</tr>`,
          )
          .join("")}</tbody></table></div>`;
      }
      if (q.type === "daterange") {
        const range = Array.isArray(selected) ? selected : ["", ""];
        return `<div class="gq-date-range"><label>${esc(t('Start'))}<input data-id="${esc(q.id)}" data-date-index="0" type="date" value="${esc(range[0] || "")}"></label><label>${esc(t('End'))}<input data-id="${esc(q.id)}" data-date-index="1" type="date" value="${esc(range[1] || "")}"></label></div>`;
      }
      if (q.type === "textarea")
        return `<textarea data-id="${esc(q.id)}" placeholder="${esc(q.placeholder || "")}" style="${q.height ? `height:${esc(q.height)};` : ""}${q.resize ? `resize:${esc(q.resize)};` : ""}" cols="${esc(q.cols || 80)}">${esc(selected || "")}</textarea>`;
      return `<input data-id="${esc(q.id)}" type="${q.type === "numeric" ? "number" : q.type === "date" ? "date" : "text"}" placeholder="${esc(q.placeholder || "")}" value="${esc(selected ?? q.selected ?? "")}" ${q.min != null ? `min="${q.min}"` : ""} ${q.max != null ? `max="${q.max}"` : ""}>`;
    }
    function collect(p) {
      for (const q of visible(p)) {
        if (["audio", "video"].includes(q.type)) continue;
        const effectiveType = q.type === "custom" ? q.base_type : q.type;
        if (q.type === "timing") {
          state.answers[q.id] = { seconds_on_page: Math.max(0, Math.round((Date.now() - (state.page_entered_at || Date.now())) / 1000)) };
          continue;
        }
        if (q.type === "rank_order") {
          const answer = Object.fromEntries([...root.querySelectorAll(`[data-q="${CSS.escape(q.id)}"] [data-rank-item]`)].filter((e) => e.value).map((e) => [scalar(e.dataset.rankItem), Number(e.value)]));
          if (Object.keys(answer).length) state.answers[q.id] = answer; else delete state.answers[q.id]; continue;
        }
        if (q.type === "constant_sum") {
          const answer = Object.fromEntries([...root.querySelectorAll(`[data-q="${CSS.escape(q.id)}"] [data-constant-item]`)].map((e) => [scalar(e.dataset.constantItem), Number(e.value || 0)]));
          state.answers[q.id] = answer; continue;
        }
        if (q.type === "side_by_side") {
          const answer = {};
          for (const column of q.columns || []) { const rows = {}; for (const row of q.rows || []) { const found = root.querySelector(`[name="${CSS.escape(q.id + ":" + column.value + ":" + row.value)}"]:checked`); if (found) rows[row.value] = scalar(found.value); } if (Object.keys(rows).length) answer[column.value] = rows; }
          if (Object.keys(answer).length) state.answers[q.id] = answer; else delete state.answers[q.id]; continue;
        }
        if (q.type === "pick_group_rank") {
          const answer = {}; for (const option of q.options || []) { const group = root.querySelector(`[data-pgr-group="${CSS.escape(String(option.value))}"]`)?.value, rank = root.querySelector(`[data-pgr-rank="${CSS.escape(String(option.value))}"]`)?.value; if (group) answer[option.value] = { group: scalar(group), rank: rank ? Number(rank) : null }; } if (Object.keys(answer).length) state.answers[q.id] = answer; else delete state.answers[q.id]; continue;
        }
        if (q.type === "drill_down") {
          const answer = [...root.querySelectorAll(`[data-q="${CSS.escape(q.id)}"] [data-drill-level]`)].map((e) => e.value).filter(Boolean); if (answer.length) state.answers[q.id] = answer; else delete state.answers[q.id]; continue;
        }
        if (["slider", "slider_numeric"].includes(effectiveType)) {
          const sliders=[...root.querySelectorAll(`[data-id="${CSS.escape(q.id)}"][type="range"]`)];
          if(sliders.length && !sliders.some(e=>e.dataset.answerInitialized==='true')) { delete state.answers[q.id];continue; }
        }
        if (effectiveType === "slider") {
          const e = root.querySelector(`[data-id="${CSS.escape(q.id)}"]`),
            option = q.options?.[Number(e?.value)];
          if (option) state.answers[q.id] = option.value;
          else delete state.answers[q.id];
          continue;
        }
        if (
          ["mc_multiple", "mc_multiple_buttons", "mc_multiple_image"].includes(
            q.type,
          )
        ) {
          const v = [
            ...root.querySelectorAll(`[name="${CSS.escape(q.id)}"]:checked`),
          ].map((x) => scalar(x.value));
          if (v.length) state.answers[q.id] = v;
          else delete state.answers[q.id];
          continue;
        }
        if (["matrix", "matrix_multiple"].includes(effectiveType)) {
          const v = {};
          for (const row of q.rows) {
            const found = [
              ...root.querySelectorAll(
                `[name="${CSS.escape(q.id + ":" + row.value)}"]:checked`,
              ),
            ];
            if (found.length)
              v[row.value] =
                effectiveType === "matrix_multiple"
                  ? found.map((e) => scalar(e.value))
                  : scalar(found[0].value);
          }
          if (Object.keys(v).length) state.answers[q.id] = v;
          continue;
        }
        if (
          q.type === "daterange" ||
          (effectiveType === "slider_numeric" &&
            root.querySelector(
              `[data-id="${CSS.escape(q.id)}"][data-range-index]`,
            ))
        ) {
          const attribute = q.type === "daterange" ? "dateIndex" : "rangeIndex";
          const values = [
            ...root.querySelectorAll(`[data-id="${CSS.escape(q.id)}"]`),
          ]
            .sort(
              (a, b) =>
                Number(a.dataset[attribute]) - Number(b.dataset[attribute]),
            )
            .map((e) => scalar(e.value));
          if (values.every((item) => item !== "")) state.answers[q.id] = values;
          else delete state.answers[q.id];
          continue;
        }
        const e =
          root.querySelector(`[name="${CSS.escape(q.id)}"]:checked`) ||
          root.querySelector(`[data-id="${CSS.escape(q.id)}"]`);
        if (e && e.value !== "") state.answers[q.id] = scalar(e.value);
        else delete state.answers[q.id];
      }
    }
    function missing(q) {
      const v = state.answers[q.id];
      const matrixType = q.type === "custom" ? q.base_type : q.type;
      return (
        q.required &&
        (v == null ||
          v === "" ||
          (Array.isArray(v) && !v.length) ||
          (["matrix", "matrix_multiple"].includes(matrixType) &&
            q.rows.some((r) => !Object.hasOwn(v || {}, r.value))))
      );
    }
    function answerProblem(q) {
      if(q.type === "custom") return answerProblem({...q,type:q.base_type});
      const v = state.answers[q.id];
      if (q.type === "rank_order" && v) {
        const ranks = Object.values(v);
        if (new Set(ranks).size !== ranks.length) return t("Use each rank only once.");
        if (q.required && ranks.length !== (q.options || []).length) return t("Rank every item.");
      }
      if (q.type === "constant_sum" && v && Object.values(v).reduce((a, b) => a + Number(b || 0), 0) !== (q.total ?? 100))
        return t("The allocation must total {total}.",{total:q.total ?? 100});
      if (q.type === "side_by_side" && q.required && (q.columns || []).some((column) => (q.rows || []).some((row) => !Object.hasOwn(v?.[column.value] || {}, row.value))))
        return t("Answer every row in every column.");
      if (q.type === "pick_group_rank" && v) {
        if (q.required && Object.keys(v).length !== (q.options || []).length) return t("Place every item in a group.");
        for (const group of q.groups || []) { const ranks = Object.values(v).filter((item) => item.group === group.value).map((item) => item.rank).filter(Boolean); if (new Set(ranks).size !== ranks.length) return t("Use each rank only once within {group}.",{group:group.label}); }
      }
      if (q.type === "drill_down" && q.required) {
        const separator = q.path_separator || " > ", valid = (q.options || []).some((option) => String(option.label).split(separator).join("\u0000") === (v || []).join("\u0000"));
        if (!valid) return t("Complete every level of the selection.");
      }
      return null;
    }
    function save() {
      if(state.lifecycle==='withdrawn' && backend.kind!=='supabase-bridge'){
        const clean=withdrawnState(state);for(const key of Object.keys(state))delete state[key];Object.assign(state,clean);
      }
      const pending = backend.save(sessionId, state);
      options.onState?.(JSON.parse(JSON.stringify(state)));
      if(pending?.then)pending.then(()=>options.onState?.(JSON.parse(JSON.stringify(state)))).catch(error=>options.onError?.(error));
      return pending;
    }
    let renderedPage = null;
    let delayTimer = null;
    let redirectTimer = null;
    let timingTimer = null;
    const questionErrors = new Map();
    function showQuestionErrors(p) {
      for(const q of visible(p)) {
        const field=card.querySelector(`[data-q="${CSS.escape(q.id)}"]`);
        if(!field)continue;
        const error=questionErrors.get(q.id), id=`${sessionId}-${q.id}-error`;
        card.querySelector(`[id="${CSS.escape(id)}"]`)?.remove();
        field.querySelectorAll('input,select,textarea').forEach(control=>{
          control.removeAttribute('aria-invalid');
          const descriptions=(control.getAttribute('aria-describedby') || '').split(' ').filter(x=>x && x!==id);
          if(error){control.setAttribute('aria-invalid','true');descriptions.push(id);}
          if(descriptions.length)control.setAttribute('aria-describedby',descriptions.join(' '));else control.removeAttribute('aria-describedby');
        });
        if(error){const note=document.createElement('p');note.id=id;note.dataset.questionError='';note.className='gq-error';note.setAttribute('role','alert');note.textContent=error;field.before(note);field.setAttribute('aria-describedby',id);}else field.removeAttribute('aria-describedby');
      }
    }
    function problems(p) {
      const result=new Map();
      for(const q of visible(p)) {
        const field=card.querySelector(`[data-q="${CSS.escape(q.id)}"]`);
        const invalid=[...(field?.querySelectorAll('input,select,textarea') || [])].find(c=>!c.validity.valid);
        const message=missing(q)?model.messages.required:answerProblem(q) || (invalid?t('Please enter a value within the allowed range and format.'):null);
        if(message)result.set(q.id,message);
      }
      for(const check of p.checks || [])if(matches(check.when)) {
        const id=check.question || check.when?.field;
        if(visible(p).some(q=>q.id===id))result.set(id,check.message);
      }
      return result;
    }
    function render(message = "") {
      if(timingTimer)clearInterval(timingTimer);
      if(redirectTimer)clearTimeout(redirectTimer);
      const p = pages.get(state.page);
      if (!p) {
        card.innerHTML = `<h1>${esc(t("Route error"))}</h1>`;
        return;
      }
      if (p.terminal) state.lifecycle = p.terminal;
      if (!state.visited.includes(p.id)) state.visited.push(p.id);
      const path =
          state.page_order || model.progress_paths?.[state.condition] ||
          model.pages.map((x) => x.id),
        pos = Math.max(0, path.indexOf(p.id)) + 1;
      progress.textContent = p.terminal
        ? t("Complete")
        : `${pos} / ${path.length}`;
      const pageChanged = renderedPage !== p.id;
      if(pageChanged)questionErrors.clear();
      renderedPage = p.id;
      if (pageChanged) state.page_entered_at = Date.now();
      if (pageChanged && p.next_delay_seconds > 0) {
        state.next_ready_page = p.id;
        state.next_ready_at = Date.now() + p.next_delay_seconds * 1000;
      }
      if (delayTimer) clearTimeout(delayTimer);
      const delayRemaining =
          state.next_ready_page === p.id
            ? Math.max(0, (state.next_ready_at || 0) - Date.now())
            : 0,
        previousMode = p.previous_mode ?? (p.show_previous === false ? "hide" : "show"),
        nextMode = p.next_mode ?? "show",
        showBack =
          !p.terminal &&
          previousMode !== "hide" &&
          (state.history.length > 0 || previousMode === "disable"),
        backDisabled = previousMode === "disable" || !state.history.length,
        showNext = !p.terminal && nextMode !== "hide",
        nextDisabled = nextMode === "disable" || delayRemaining > 0;
      card.innerHTML = `<p class="gq-eyebrow">${esc(model.title)}</p><h1>${esc(p.title)}</h1><div class="gq-copy">${inlineMarkdown(p.body || "")}</div>${visible(
        p,
      )
        .map(
          (q) =>
            `<fieldset class="gq-q gq-${esc(q.type)} gq-direction-${esc(q.direction || "horizontal")}${q.justified ? " gq-justified" : ""}" data-q="${esc(q.id)}" style="${q.width ? `width:${esc(q.width)}` : ""}"><legend>${inlineMarkdown(q.label)}${q.required ? ` <span aria-label="${esc(t('required'))}">*</span>` : ""}</legend>${input(q)}</fieldset>`,
        )
        .join(
          "",
        )}${message ? `<p class="gq-error" role="alert">${esc(message)}</p>` : ""}<div class="gq-actions">${showBack ? `<button data-back ${backDisabled ? "disabled" : ""}>${esc(model.messages.previous)}</button>` : ""}${p.terminal ? `<strong>${esc(t(p.terminal))}</strong>` : showNext ? `<button data-next ${nextDisabled ? "disabled" : ""}>${esc(p.next_label || model.messages.next)}${delayRemaining > 0 ? ` (${Math.ceil(delayRemaining / 1000)}${esc(t('s'))})` : ""}</button>` : ""}</div>`;
      if (delayRemaining > 0 && nextMode !== "disable")
        delayTimer = setTimeout(() => render(message), Math.min(1000, delayRemaining));
      const back = card.querySelector("[data-back]");
      for(const q of visible(p)) {
        const field=card.querySelector(`[data-q="${CSS.escape(q.id)}"]`),type=q.type==='custom'?q.base_type:q.type;
        if(['mc_multiple','mc_multiple_buttons','mc_multiple_image','select_multiple','matrix_multiple'].includes(type) && q.selection_hint!==false && q.selection_hint!=='') {
          const hint=document.createElement('p');hint.className='gq-selection-hint';hint.textContent=typeof q.selection_hint==='string'?q.selection_hint:t('Select all that apply.');field.insertBefore(hint,field.querySelector('legend').nextSibling);
        }
        if(type==='timing' && options.preview===true) {
          const note=document.createElement('div');note.className='gq-timing-preview';note.innerHTML='<output data-timing-preview></output><p></p>';note.querySelector('p').textContent=t('(Timer running in the background; nothing is shown to participants.)');field.append(note);
        }
        if(type==='timing' && options.preview!==true)field.hidden=true;
      }
      const tick=()=>card.querySelectorAll('[data-timing-preview]').forEach(e=>{const ms=Math.max(0,Date.now()-state.page_entered_at);e.textContent=`${String(Math.floor(ms/60000)).padStart(2,'0')}:${String(Math.floor(ms/1000)%60).padStart(2,'0')}.${String(ms%1000).padStart(3,'0')}`;});
      if(card.querySelector('[data-timing-preview]')){tick();timingTimer=setInterval(()=>{if(!card.isConnected){clearInterval(timingTimer);return;}tick();},47);}
      showQuestionErrors(p);
      if(p.terminal && p.redirect) {
        const button=root.ownerDocument.createElement("button");button.textContent=t(p.redirect.label);
        button.dataset.redirect="";button.disabled=true;card.querySelector(".gq-actions").append(button);
        const prolificPath=Object.values(model.runtime_policy?.prolific?.paths || {}).find(path=>path.page===p.id);
        const enabled=options.allowExternalRedirects===true && (!prolificPath || options.allowProlificReturns===true);
        if(!enabled)button.textContent+=t(" (preview: no external navigation)");
        Promise.resolve(save()).then(saved=>{
          if(!enabled || saved?.status==="conflict" || state.page!==p.id || !button.isConnected)return;
          let url;try {url=redirectUrl(p.redirect,root.ownerDocument.defaultView.location.search);}catch(e){button.textContent=t("Return link unavailable.");return;}
          button.disabled=false;
          if(prolificPath){const note=root.ownerDocument.createElement('p');note.dataset.completionCode='';note.textContent=t('Completion code')+': '+prolificPath.code;button.before(note);}
          button.onclick=()=>{
            if(p.redirect.newtab)root.ownerDocument.defaultView.open(url,"_blank","noopener,noreferrer");
            else root.ownerDocument.defaultView.location.assign(url);
          };
          if(p.redirect.delay!==null)redirectTimer=setTimeout(()=>{if(state.page===p.id && button.isConnected)button.click();},p.redirect.delay*1000);
        }).catch(()=>{button.textContent=t("Response not saved. Please retry before leaving.");});
      }
      if (back)
        back.onclick = () => {
          collect(p);
          state.page = state.history.pop();
          save();
          render();
        };
      for (const slider of card.querySelectorAll('input[type="range"]'))
        slider.oninput = () => {
          slider.dataset.answerInitialized="true";
          const question = (p.questions || []).find(
              (item) => item.id === slider.dataset.id,
            ),
            output = card.querySelector(
              `[data-slider-output="${CSS.escape(slider.dataset.id)}"]`,
            );
          if (output) {
            if (slider.dataset.sliderKind === "categorical")
              output.textContent =
                question?.options?.[Number(slider.value)]?.label || "";
            else if (slider.dataset.sliderKind === "numeric-range") {
              const sliders = [
                ...card.querySelectorAll(
                  `[data-id="${CSS.escape(slider.dataset.id)}"][data-range-index]`,
                ),
              ].sort(
                (a, b) =>
                  Number(a.dataset.rangeIndex) - Number(b.dataset.rangeIndex),
              );
              if (Number(sliders[0].value) > Number(sliders[1].value))
                slider.value =
                  sliders[Number(slider.dataset.rangeIndex) ? 0 : 1].value;
              output.textContent = sliders
                .map((item) => item.value)
                .join(question?.sep || " – ");
            } else output.textContent = `${question?.pre || ""}${slider.value}`;
          }
        };
      for (const sum of card.querySelectorAll(".gq-constant-sum")) {
        const updateSum = () => { const values = [...sum.querySelectorAll("[data-constant-item]")].map((e) => Number(e.value || 0)); const qid = sum.closest("[data-q]")?.dataset.q, question = (p.questions || []).find((item) => item.id === qid), total = question?.total ?? 100, value=values.reduce((a,b)=>a+b,0), output=sum.querySelector('[data-constant-total]'); output.textContent=`${value} / ${total}`;output.classList.toggle('gq-total-warning',Math.abs(value-total)>1e-8 || values.some(v=>v<0));output.setAttribute('aria-live','polite'); };
        sum.addEventListener("input", updateSum); updateSum();
      }
      for (const drill of card.querySelectorAll(".gq-drill-down select"))
        drill.addEventListener("change", () => { collect(p); save(); render(); });
      const ruleFields=r=>!r?[]:r.field?[r.field]:r.not?ruleFields(r.not):(r.all || r.any || []).flatMap(ruleFields);
      const visibilitySources = new Set((p.questions || []).flatMap(question=>ruleFields(question.show_if)));
      for (const control of card.querySelectorAll("input,select,textarea"))
        control.addEventListener("change", () => {
          const source = control.name?.split(":")[0] || control.dataset.id;
          collect(p);
          save();
          if (visibilitySources.has(source)) render();
        });
      const next = card.querySelector("[data-next]");
      card.oninput=card.onchange=(event)=>{collect(p);const current=problems(p);for(const id of questionErrors.keys()){if(current.has(id))questionErrors.set(id,current.get(id));else questionErrors.delete(id);}showQuestionErrors(p);const field=event.target.closest('[data-q]'),q=visible(p).find(item=>item.id===field?.dataset.q);if(q){const controls=[...field.querySelectorAll('input,select,textarea')],invalid=controls.some(c=>c.value!=='' && !c.validity.valid) || !!answerProblem(q);field.classList.toggle('gq-answer-warning',invalid);}};
      if (next)
        next.onclick = async () => {
          if (next.disabled) return;
          collect(p);
          for (const q of p.questions || [])
            if (q.show_if && !matches(q.show_if)) delete state.answers[q.id];
          questionErrors.clear();for(const [id,error] of problems(p))questionErrors.set(id,error);
          if(questionErrors.size){showQuestionErrors(p);const first=visible(p).find(q=>questionErrors.has(q.id)),field=card.querySelector(`[data-q="${CSS.escape(first.id)}"]`);field.tabIndex=-1;field.focus({preventScroll:true});(field.previousElementSibling?.matches('[data-question-error]')?field.previousElementSibling:field).scrollIntoView({block:'start',behavior:'auto'});return;}
          const stopped=(p.checks || []).find(check=>matches(check.when));
          if(stopped){render(stopped.message);return;}
          if (model.assignment_page === p.id && !state.condition) {
            if (model.runtime_policy?.consent && !state.consent_accepted) { render(t("Please confirm consent before random assignment.")); return; }
            next.disabled = true;
            try {
              const saved=await save();
              if(saved?.status==="conflict")throw new Error("A newer preview tab has already saved this session.");
              state.condition = await backend.assign(sessionId, model.conditions, model.randomization, JSON.stringify([model.study_id,model.runtime_policy?.mode || "test"]));
            } catch(error) {
              render(t("Random assignment could not be completed. Please try again.")); options.onError?.(error); return;
            }
          }
          const target = nextFor(p);
          if (!target || !pages.has(target)) {
            render(t("The next page is unavailable."));
            return;
          }
          state.history.push(p.id);
          state.page = target;
          next.disabled = true;
          try { const saved=await save(); if(saved?.status==="conflict")throw new Error("A newer preview tab has already saved this session."); } catch(error) {
            state.page = state.history.pop();
            render(t("Your response could not be saved. Please try again.")); return;
          }
          render();
        };
      save();
      if (pageChanged)
        requestAnimationFrame(() => {
          const scroller = root.closest(".screen,.viewport");
          if (scroller)
            scroller.scrollTo({ top: 0, left: 0, behavior: "auto" });
          else root.scrollIntoView({ block: "start", behavior: "auto" });
        });
    }
    render();
    return {
      mode,
      sessionId,
      state,
      render,
      reset() {
        backend.clear(sessionId);
        Object.assign(state, fresh());
        render();
      },
      async withdraw() {
        try{
          await backend.clear(sessionId);
          const ending=model.pages.find(page=>page.terminal==='withdrawn');
          const clean=withdrawnState({...state,page:ending?.id || state.page});
          for(const key of Object.keys(state))delete state[key];Object.assign(state,clean);
          if(ending)render();else card.innerHTML=`<h1>${esc(t("Participation withdrawn"))}</h1>`;
        }catch(error){render(t('Your response could not be saved. Please try again.'));options.onError?.(error);throw error;}
      },
      backend,
    };
  }
  function mountRespondentSafe(root, model, options = {}) {
    const source = options.backend || createMemoryBackend();
    const controller = mountRespondent(root, model, {
      ...options,
      backend: source,
    });
    root.addEventListener(
      "click",
      async (event) => {
        if (!event.target.closest("[data-next]")) return;
        const page = model.pages.find(
          (item) => item.id === controller.state.page,
        );
        const consent = model.runtime_policy?.consent;
        if (
          consent &&
          page?.questions?.some((question) => question.id === consent.question)
        ) {
          const selected = root.querySelector(
            `[name="${CSS.escape(consent.question)}"]:checked`,
          );
          controller.state.consent_accepted = selected
            ? scalar(selected.value) === consent.accept_value
            : false;
        }
      },
      true,
    );
    return controller;
  }
  async function mountSupabaseRespondent(
    root,
    model,
    { url, anonKey, sessionId, externalIdentifiers, previewToken, onError } = {},
  ) {
    if(previewToken && (model.runtime_policy?.mode!=='test' || !externalIdentifiers))throw new Error('Preview grants require a Prolific test launch.');
    const storageKey = `greedyq-capability:${JSON.stringify([model.study_id,model.runtime_policy?.mode || 'test',externalIdentifiers || 'direct',...(previewToken?[previewToken]:[])])}`,
      saved = JSON.parse(localStorage.getItem(storageKey) || "null"),
      id = saved?.id || (previewToken?crypto.randomUUID():sessionId) || crypto.randomUUID(),
      accessToken =
        saved?.accessToken || `${crypto.randomUUID()}${crypto.randomUUID()}`;
    localStorage.setItem(storageKey, JSON.stringify({ id, accessToken }));
    const remote = createSecureSupabaseBackend({
      url,
      anonKey,
      accessToken,
      studyId: model.study_id,
      studyVersion: model.study_version,
      greedyqVersion: model.greedyq_version,
      specVersion: "0.2",
      isTest: model.runtime_policy?.mode !== "production",
      consentQuestion: model.runtime_policy?.consent?.question,
    });
    if(externalIdentifiers)await remote.startProlific(id,externalIdentifiers,previewToken);
    else await remote.create(id);
    const loaded = await remote.load(id),
      memory = createMemoryBackend();
    const canonical=value=>JSON.stringify(value && typeof value==='object'
      ? Array.isArray(value) ? value.map(x=>JSON.parse(canonical(x))) : Object.fromEntries(Object.keys(value).sort().map(k=>[k,JSON.parse(canonical(value[k]))]))
      : value);
    if (loaded?.runtime_contract !== "randomization-1" || canonical(loaded.registered_model)!==canonical(model))
      throw new Error("The registered study and browser runtime do not match. The researcher must finish the database upgrade and register this study before collecting responses.");
    if (loaded?.state && typeof loaded.state.page === "string")
      memory.save(id, {
        ...loaded.state,
        condition: loaded.condition ?? loaded.state.condition ?? null,
      });
    else if (typeof loaded?.page === "string") memory.save(id, loaded);
    let pending = Promise.resolve(), acknowledged=loaded?.state || null;
    const bridge = {
      kind: "supabase-bridge",
      load: memory.load,
      assign: (sid, conditions) =>
        remote.assign(sid, conditions),
      inspect: memory.inspect,
      save: (sid, state) => {
        memory.save(sid, state);
        const persistedState = {
          ...JSON.parse(JSON.stringify(state)),
          lifecycle:
            state.lifecycle === "active"
              ? state.consent_accepted
                ? "in_progress"
                : "created"
              : state.lifecycle,
        };
        pending = pending.catch(()=>{}).then(async()=>{
          // Withdrawal is irreversible. Discard queued pre-erasure snapshots
          // and reuse the clean receipt on terminal re-render/reload.
          if(acknowledged?.lifecycle==='withdrawn' && persistedState.lifecycle==='withdrawn'){
            for(const key of Object.keys(state))delete state[key];Object.assign(state,acknowledged);memory.save(sid,acknowledged);return;
          }
          await remote.save(sid,persistedState);
          if(persistedState.lifecycle==='withdrawn'){
            const receipt=await remote.load(sid);
            if(receipt?.state?.lifecycle!=='withdrawn' || Object.keys(receipt.state.answers || {}).length)throw new Error('Withdrawal erasure was not acknowledged.');
            for(const key of Object.keys(state))delete state[key];Object.assign(state,receipt.state);memory.save(sid,receipt.state);acknowledged=receipt.state;
          }else acknowledged=persistedState;
        });
        pending.catch((error) => onError?.(error));
        return pending;
      },
      clear: (sid) => {
        pending=pending.catch(()=>{}).then(async()=>{
          await remote.clear(sid);const receipt=await remote.load(sid);
          if(receipt?.state?.lifecycle!=='withdrawn' || Object.keys(receipt.state.answers || {}).length)throw new Error('Withdrawal erasure was not acknowledged.');
          memory.save(sid,receipt.state);acknowledged=receipt.state;
        });
        pending.catch((error)=>onError?.(error));return pending;
      },
    };
    return mountRespondentSafe(root, model, {
      allowExternalRedirects: true,
      allowProlificReturns:!!externalIdentifiers,
      mode: detectDevice(root.ownerDocument.defaultView),
      backend: bridge,
      sessionId: id,
      onState: (state) => state,
      onError,
    });
  }
  return {
    VERSION, RELEASE, condition, matchesCondition, inlineMarkdown, translate,
    planProblem, orderingProblems, drawAssignment, shuffle, questionOrder, optionPlan, optionOrder, pagePlan, pageOrder, redirectPlan, redirectUrl,
    ParseError,
    parseYaml,
    parseSurvey,
    validateSurvey: validateSurveyComplete,
    compileSurvey,
    detectDevice,
    parseProlificLaunch, prolificPlan,
    resolveProlificLaunch,
    stableSessionId,
    createMemoryBackend,
    createLocalMockBackend: createConcurrentLocalMockBackend,
    createSupabaseBackend: createSecureSupabaseBackend,
    mountRespondent: mountRespondentSafe,
    mountSupabaseRespondent,
  };
});

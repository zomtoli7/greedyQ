/* greedyQ browser core v0.2.0-draft.1. Copy byte-for-byte; do not customize. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  root.greedyQ = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  const VERSION = "0.2.0-draft.1";
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
          if (args.image) q.images = args.image.map((item) => item.value);
          if (["mc_image", "mc_multiple_image"].includes(q.type))
            for (const option of q.options || [])
              option.caption = option._named !== false;
          for (const option of [...(q.options || []), ...(q.rows || [])])
            delete option._named;
          if (args.label_select) q.placeholder = args.label_select;
          for (const key of [
            "option",
            "options",
            "row",
            "rows",
            "label_select",
            "image",
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
            "pre",
            "sep",
            "animate",
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
    if (parsed.front_matter?.greedyq?.spec_version !== "0.2")
      issues.push(
        issue("GQ003", "Set the survey specification version to 0.2.", qmd, 1),
      );
    if (config.spec_version !== "0.2")
      issues.push(
        issue("GQ003", "Set the study settings version to 0.2.", yml, 1),
      );
    const organization = parsed.front_matter?.greedyq?.organization;
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
        greedyq: new Set(["spec_version", "organization"]),
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
      for (const collection of ["options", "rows"]) {
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
    for (const randomization of config.randomization || []) {
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
    for (const [name, outcome] of Object.entries(config.outcomes || {}))
      if (outcome.redirect && !String(outcome.redirect).startsWith("https://"))
        issues.push(
          issue(
            "GQ009",
            `The '${name}' redirect must use a secure https address.`,
            yml,
          ),
        );
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
  function condition(expression) {
    const s = String(expression).trim();
    for (const [c, key] of [
      [" and ", "all"],
      [" or ", "any"],
    ])
      if (s.includes(c)) return { [key]: s.split(c).map(condition) };
    for (const [token, key] of OPS)
      if (s.includes(token)) {
        let [field, value] = s.split(token, 2);
        field =
          field.trim() === "assignment_condition" ? "condition" : field.trim();
        return { field, [key]: scalar(value) };
      }
    return { unsupported: s };
  }
  function compileSurvey(parsed, config) {
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
          q.required = required.has(q.id);
          const show = shows.find((x) => x.question === q.id);
          if (show) q.show_if = condition(show.if);
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
      page.next = nav.page_next || (parsed.pages[index + 1]?.id ?? null);
      if (nav.label_next) page.next_label = nav.label_next;
      const routes = skips
        .filter((x) => x.from === page.id)
        .map((x) => ({ when: condition(x.if), to: x.to }));
      if (routes.length) page.routes = routes;
      if (term[page.id]) {
        delete page.next;
        page.terminal = term[page.id];
      }
      return page;
    });
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
      title: config.study?.title || front.title || "greedyQ Survey",
      organization: front.greedyq?.organization || "Research team",
      start_page: start,
      brand_color: front["theme-settings"]?.barcolor || "#315c8a",
      messages: {
        previous: front["system-messages"]?.previous || "Previous",
        next: front["system-messages"]?.next || "Continue",
        required:
          front["system-messages"]?.required ||
          "Please answer the required questions before continuing.",
      },
      conditions: conditions.length ? conditions : ["default"],
      progress_paths: paths,
      pages,
      runtime_policy: {
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
  function createMemoryBackend() {
    const sessions = new Map(),
      allocations = [];
    return {
      kind: "memory",
      load: (id) => sessions.get(id) || null,
      save: (id, state) => sessions.set(id, JSON.parse(JSON.stringify(state))),
      clear: (id) => sessions.delete(id),
      assign: (id, conditions) => {
        const existing = allocations.find((x) => x.id === id);
        if (existing) return existing.condition;
        const counts = Object.fromEntries(
            conditions.map((c) => [
              c,
              allocations.filter((x) => x.condition === c).length,
            ]),
          ),
          min = Math.min(...Object.values(counts)),
          candidates = conditions.filter((c) => counts[c] === min),
          condition = candidates[allocations.length % candidates.length];
        allocations.push({ id, condition });
        return condition;
      },
      inspect: () => ({
        sessions: [...sessions.entries()],
        allocations: [...allocations],
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
    const key = `${namespace}:state`,
      empty = () => ({ sessions: [], allocations: [] }),
      read = () => {
        try {
          return JSON.parse(localStorage.getItem(key) || "null") || empty();
        } catch {
          return empty();
        }
      },
      write = (data) => localStorage.setItem(key, JSON.stringify(data)),
      clone = (value) =>
        value == null ? null : JSON.parse(JSON.stringify(value));
    return {
      kind: "local-mock",
      load(id) {
        const found = read().sessions.find((item) => item[0] === id);
        return found ? clone(found[1]) : null;
      },
      save(id, state) {
        const data = read(),
          index = data.sessions.findIndex((item) => item[0] === id),
          current = index < 0 ? null : data.sessions[index][1],
          expected = Number(state._revision || 0);
        if (current && Number(current._revision || 0) !== expected)
          return { status: "conflict", current: clone(current) };
        const saved = clone(state);
        saved._revision = expected + 1;
        state._revision = saved._revision;
        if (index < 0) data.sessions.push([id, saved]);
        else data.sessions[index] = [id, saved];
        write(data);
        return { status: "saved", revision: saved._revision };
      },
      clear(id) {
        const data = read();
        data.sessions = data.sessions.filter((item) => item[0] !== id);
        data.allocations = data.allocations.filter((item) => item.id !== id);
        write(data);
        return { status: "deleted" };
      },
      assign(id, conditions) {
        const data = read(),
          existing = data.allocations.find((item) => item.id === id);
        if (existing) return existing.condition;
        const counts = Object.fromEntries(
            conditions.map((condition) => [
              condition,
              data.allocations.filter((item) => item.condition === condition)
                .length,
            ]),
          ),
          minimum = Math.min(...Object.values(counts)),
          candidates = conditions.filter(
            (condition) => counts[condition] === minimum,
          ),
          condition = candidates[data.allocations.length % candidates.length];
        data.allocations.push({ id, condition });
        write(data);
        return condition;
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
        if (!response.ok)
          throw new Error(`Supabase RPC ${name} failed (${response.status}).`);
        return response.status === 204 ? null : response.json();
      };
    return {
      kind: "supabase-secure",
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
          p_conditions: conditions,
          p_is_test: isTest,
        }),
      raw: base,
    };
  }
  function parseProlificLaunch(search, mode = "test") {
    const params = new URLSearchParams(String(search).replace(/^\?/, "")),
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
    }
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
  function stableSessionId(studyId, provided) {
    const key = `greedyq-session:${studyId}`;
    if (provided) {
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
  function mountRespondent(root, model, options = {}) {
    const mode = options.mode || detectDevice(root.ownerDocument.defaultView),
      backend = options.backend || createMemoryBackend(),
      sessionId =
        options.sessionId || `virtual-${Math.random().toString(36).slice(2)}`,
      pages = new Map(model.pages.map((p) => [p.id, p])),
      fresh = () => ({
        page: model.start_page,
        history: [],
        answers: {},
        condition: backend.assign(sessionId, model.conditions || ["default"]),
        lifecycle: "active",
        visited: [],
      }),
      state = backend.load(sessionId) || fresh();
    root.className = `gq-app gq-${mode}`;
    root.innerHTML = `<div class="gq-top"><b>${esc(model.organization || "Research team")}</b><span class="gq-progress"></span></div><main class="gq-card" aria-live="polite"></main>`;
    const card = root.querySelector(".gq-card"),
      progress = root.querySelector(".gq-progress");
    const value = (f) =>
        f === "condition" ? state.condition : state.answers[f],
      matches = (r) =>
        !r
          ? true
          : r.all
            ? r.all.every(matches)
            : r.any
              ? r.any.some(matches)
              : "equals" in r
                ? value(r.field) === r.equals
                : "not_equals" in r
                  ? value(r.field) !== r.not_equals
                  : "lt" in r
                    ? Number(value(r.field)) < r.lt
                    : "lte" in r
                      ? Number(value(r.field)) <= r.lte
                      : "gt" in r
                        ? Number(value(r.field)) > r.gt
                        : "gte" in r
                          ? Number(value(r.field)) >= r.gte
                          : false,
      visible = (p) => (p.questions || []).filter((q) => matches(q.show_if)),
      nextFor = (p) =>
        (p.routes || []).find((r) => matches(r.when))?.to ?? p.next;
    function input(q) {
      const selected = state.answers[q.id],
        initial = selected ?? q.selected,
        today = new Date().toISOString().slice(0, 10);
      if (["mc", "mc_buttons", "mc_image"].includes(q.type))
        return (q.options || [])
          .map(
            (o, index) =>
              `<label class="gq-choice${q.type === "mc_buttons" ? " gq-button-choice" : ""}${q.type === "mc_image" ? " gq-image-choice" : ""}"><input type="radio" name="${esc(q.id)}" value="${esc(o.value)}" ${initial === o.value ? "checked" : ""}>${q.type === "mc_image" ? `<img src="${esc(q.images?.[index] || "")}" alt="${esc(o.label || "Option " + (index + 1))}">` : ""}${q.type !== "mc_image" || o.caption !== false ? `<span>${esc(o.label)}</span>` : ""}</label>`,
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
        return `<div class="gq-slider gq-slider-${esc(orientation)}"><output id="${esc(outputId)}" for="${esc(inputId)}" aria-live="polite" data-slider-output="${esc(q.id)}">${esc(options[index]?.label || "")}</output><input id="${esc(inputId)}" aria-label="${esc(q.label)}" aria-describedby="${esc(outputId)}" data-id="${esc(q.id)}" data-slider-kind="categorical" type="range" min="0" max="${Math.max(0, options.length - 1)}" step="1" value="${index}"><div class="gq-slider-labels"><span>${esc(options[0]?.label || "")}</span><span>${esc(options.at(-1)?.label || "")}</span></div></div>`;
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
          return `<div class="gq-slider gq-slider-range"><output id="${esc(outputId)}" aria-live="polite" data-slider-output="${esc(q.id)}">${esc(range.join(q.sep || " – "))}</output><input aria-label="${esc(q.label)} minimum" aria-describedby="${esc(outputId)}" data-id="${esc(q.id)}" data-range-index="0" data-slider-kind="numeric-range" type="range" min="${esc(min)}" max="${esc(max)}" step="${esc(step)}" value="${esc(range[0])}"><input aria-label="${esc(q.label)} maximum" aria-describedby="${esc(outputId)}" data-id="${esc(q.id)}" data-range-index="1" data-slider-kind="numeric-range" type="range" min="${esc(min)}" max="${esc(max)}" step="${esc(step)}" value="${esc(range[1])}"><div class="gq-slider-labels"><span>${esc(min)}</span><span>${esc(max)}</span></div></div>`;
        }
        return `<div class="gq-slider gq-slider-${esc(orientation)}"><output id="${esc(outputId)}" for="${esc(inputId)}" aria-live="polite" data-slider-output="${esc(q.id)}">${esc((q.pre || "") + current)}</output><input id="${esc(inputId)}" aria-label="${esc(q.label)}" aria-describedby="${esc(outputId)}" data-id="${esc(q.id)}" data-slider-kind="numeric" type="range" min="${esc(min)}" max="${esc(max)}" step="${esc(step)}" value="${esc(current)}"><div class="gq-slider-labels"><span>${esc(min)}</span><span>${esc(max)}</span></div></div>`;
      }
      if (
        ["mc_multiple", "mc_multiple_buttons", "mc_multiple_image"].includes(
          q.type,
        )
      )
        return (q.options || [])
          .map(
            (o, index) =>
              `<label class="gq-choice${q.type === "mc_multiple_buttons" ? " gq-button-choice" : ""}${q.type === "mc_multiple_image" ? " gq-image-choice" : ""}"><input type="checkbox" name="${esc(q.id)}" value="${esc(o.value)}" ${Array.isArray(initial) && initial.includes(o.value) ? "checked" : ""}>${q.type === "mc_multiple_image" ? `<img src="${esc(q.images?.[index] || "")}" alt="${esc(o.label || "Option " + (index + 1))}">` : ""}${q.type !== "mc_multiple_image" || o.caption !== false ? `<span>${esc(o.label)}</span>` : ""}</label>`,
          )
          .join("");
      if (q.type === "select")
        return `<select data-id="${esc(q.id)}"><option value="">${esc(q.placeholder || "Choose one")}</option>${q.options.map((o) => `<option value="${esc(o.value)}" ${selected === o.value ? "selected" : ""}>${esc(o.label)}</option>`).join("")}</select>`;
      if (["matrix", "matrix_multiple"].includes(q.type))
        return `<div class="gq-matrix">${q.rows.map((r) => `<fieldset><legend>${esc(r.label)}</legend>${q.options.map((o) => `<label><input type="${q.type === "matrix_multiple" ? "checkbox" : "radio"}" name="${esc(q.id + ":" + r.value)}" value="${esc(o.value)}" ${q.type === "matrix_multiple" ? (Array.isArray(selected?.[r.value]) && selected[r.value].includes(o.value) ? "checked" : "") : selected?.[r.value] === o.value ? "checked" : ""}>${esc(o.label)}</label>`).join("")}</fieldset>`).join("")}</div>`;
      if (q.type === "daterange") {
        const range = Array.isArray(selected) ? selected : ["", ""];
        return `<div class="gq-date-range"><label>Start<input data-id="${esc(q.id)}" data-date-index="0" type="date" value="${esc(range[0] || "")}"></label><label>End<input data-id="${esc(q.id)}" data-date-index="1" type="date" value="${esc(range[1] || "")}"></label></div>`;
      }
      if (q.type === "textarea")
        return `<textarea data-id="${esc(q.id)}" placeholder="${esc(q.placeholder || "")}" style="${q.height ? `height:${esc(q.height)};` : ""}${q.resize ? `resize:${esc(q.resize)};` : ""}" cols="${esc(q.cols || 80)}">${esc(selected || "")}</textarea>`;
      return `<input data-id="${esc(q.id)}" type="${q.type === "numeric" ? "number" : q.type === "date" ? "date" : "text"}" placeholder="${esc(q.placeholder || "")}" value="${esc(selected ?? q.selected ?? (q.type === "date" ? today : ""))}" ${q.min != null ? `min="${q.min}"` : ""} ${q.max != null ? `max="${q.max}"` : ""}>`;
    }
    function collect(p) {
      for (const q of visible(p)) {
        if (q.type === "slider") {
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
        if (["matrix", "matrix_multiple"].includes(q.type)) {
          const v = {};
          for (const row of q.rows) {
            const found = [
              ...root.querySelectorAll(
                `[name="${CSS.escape(q.id + ":" + row.value)}"]:checked`,
              ),
            ];
            if (found.length)
              v[row.value] =
                q.type === "matrix_multiple"
                  ? found.map((e) => scalar(e.value))
                  : scalar(found[0].value);
          }
          if (Object.keys(v).length) state.answers[q.id] = v;
          continue;
        }
        if (
          q.type === "daterange" ||
          (q.type === "slider_numeric" &&
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
      return (
        q.required &&
        (v == null ||
          v === "" ||
          (Array.isArray(v) && !v.length) ||
          (["matrix", "matrix_multiple"].includes(q.type) &&
            q.rows.some((r) => !Object.hasOwn(v || {}, r.value))))
      );
    }
    function save() {
      backend.save(sessionId, state);
      options.onState?.(JSON.parse(JSON.stringify(state)));
    }
    let renderedPage = null;
    function render(message = "") {
      const p = pages.get(state.page);
      if (!p) {
        card.innerHTML = "<h1>Route error</h1>";
        return;
      }
      if (p.terminal) state.lifecycle = p.terminal;
      if (!state.visited.includes(p.id)) state.visited.push(p.id);
      const path =
          model.progress_paths?.[state.condition] ||
          model.pages.map((x) => x.id),
        pos = Math.max(0, path.indexOf(p.id)) + 1;
      progress.textContent = p.terminal
        ? "Complete"
        : `${pos} / ${path.length}`;
      const pageChanged = renderedPage !== p.id;
      renderedPage = p.id;
      card.innerHTML = `<p class="gq-eyebrow">${esc(model.title)}</p><h1>${esc(p.title)}</h1><div class="gq-copy">${esc(p.body || "")}</div>${visible(
        p,
      )
        .map(
          (q) =>
            `<fieldset class="gq-q gq-${esc(q.type)} gq-direction-${esc(q.direction || "horizontal")}${q.justified ? " gq-justified" : ""}" data-q="${esc(q.id)}" style="${q.width ? `width:${esc(q.width)}` : ""}"><legend>${esc(q.label)}${q.required ? ' <span aria-label="required">*</span>' : ""}</legend>${input(q)}</fieldset>`,
        )
        .join(
          "",
        )}${message ? `<p class="gq-error" role="alert">${esc(message)}</p>` : ""}<div class="gq-actions">${state.history.length && p.show_previous !== false && !p.terminal ? `<button data-back>${esc(model.messages.previous)}</button>` : ""}${p.terminal ? `<strong>${esc(p.terminal)}</strong>` : `<button data-next>${esc(p.next_label || model.messages.next)}</button>`}</div>`;
      const back = card.querySelector("[data-back]");
      if (back)
        back.onclick = () => {
          collect(p);
          state.page = state.history.pop();
          save();
          render();
        };
      for (const slider of card.querySelectorAll('input[type="range"]'))
        slider.oninput = () => {
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
      const next = card.querySelector("[data-next]");
      if (next)
        next.onclick = () => {
          collect(p);
          for (const q of p.questions || [])
            if (q.show_if && !matches(q.show_if)) delete state.answers[q.id];
          const invalid = visible(p).find(missing);
          if (invalid) {
            render(`${model.messages.required} ${invalid.label}`);
            card
              .querySelector(
                `[data-q="${CSS.escape(invalid.id)}"] input,[data-q="${CSS.escape(invalid.id)}"] select,[data-q="${CSS.escape(invalid.id)}"] textarea`,
              )
              ?.focus();
            return;
          }
          const target = nextFor(p);
          if (!target || !pages.has(target)) {
            render("The next page is unavailable.");
            return;
          }
          state.history.push(p.id);
          state.page = target;
          save();
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
      withdraw() {
        backend.clear(sessionId);
        state.lifecycle = "withdrawn";
        card.innerHTML = "<h1>Participation withdrawn</h1>";
      },
      backend,
    };
  }
  function mountRespondentSafe(root, model, options = {}) {
    const source = options.backend || createMemoryBackend();
    let assignmentAllowed = !model.assignment_page,
      assignmentRetry = false;
    const deferred = {
      ...source,
      assign: (id, conditions) =>
        assignmentAllowed ? source.assign(id, conditions) : null,
    };
    const controller = mountRespondent(root, model, {
      ...options,
      backend: deferred,
    });
    const reset = controller.reset;
    controller.reset = () => {
      assignmentAllowed = !model.assignment_page;
      assignmentRetry = false;
      reset();
    };
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
        for (const question of page?.questions || []) {
          if (!["numeric", "slider_numeric"].includes(question.type)) continue;
          const input = root.querySelector(
            `[data-id="${CSS.escape(question.id)}"]`,
          );
          if (!input || input.value === "") continue;
          const value = Number(input.value),
            tooLow = question.min != null && value < question.min,
            tooHigh = question.max != null && value > question.max;
          if (tooLow || tooHigh) {
            event.preventDefault();
            event.stopImmediatePropagation();
            const boundary = tooLow
              ? `at least ${question.min}`
              : `at most ${question.max}`;
            controller.render(`${question.label} must be ${boundary}.`);
            root
              .querySelector(`[data-id="${CSS.escape(question.id)}"]`)
              ?.focus();
            return;
          }
        }
        if (
          model.assignment_page === page?.id &&
          !controller.state.condition &&
          !assignmentRetry
        ) {
          assignmentAllowed = true;
          const assigned = source.assign(
            controller.sessionId,
            model.conditions || ["default"],
          );
          if (assigned && typeof assigned.then === "function") {
            event.preventDefault();
            event.stopImmediatePropagation();
            assignmentRetry = true;
            assigned
              .then((condition) => {
                controller.state.condition = condition;
                assignmentRetry = false;
                event.target.closest("[data-next]")?.click();
              })
              .catch((error) => {
                assignmentRetry = false;
                controller.render(
                  "Random assignment could not be completed. Please try again.",
                );
                options.onError?.(error);
              });
          } else controller.state.condition = assigned;
        }
      },
      true,
    );
    return controller;
  }
  async function mountSupabaseRespondent(
    root,
    model,
    { url, anonKey, sessionId, onError } = {},
  ) {
    const storageKey = `greedyq-capability:${model.study_id}`,
      saved = JSON.parse(localStorage.getItem(storageKey) || "null"),
      id = saved?.id || sessionId || crypto.randomUUID(),
      accessToken =
        saved?.accessToken || `${crypto.randomUUID()}${crypto.randomUUID()}`;
    localStorage.setItem(storageKey, JSON.stringify({ id, accessToken }));
    const remote = createSecureSupabaseBackend({
        url,
        anonKey,
        accessToken,
        studyId: model.study_id,
        specVersion: "0.2",
        isTest: model.runtime_policy?.mode !== "production",
        consentQuestion: model.runtime_policy?.consent?.question,
      }),
      loaded = await remote.load(id),
      memory = createMemoryBackend();
    if (loaded?.state)
      memory.save(id, {
        ...loaded.state,
        condition: loaded.condition ?? loaded.state.condition ?? null,
      });
    else if (loaded?.page) memory.save(id, loaded);
    const bridge = {
      kind: "supabase-bridge",
      load: memory.load,
      assign: (sid, conditions) => remote.assign(sid, conditions),
      inspect: memory.inspect,
      save: (sid, state) => {
        memory.save(sid, state);
        remote.save(sid, state).catch((error) => onError?.(error));
      },
      clear: (sid) => {
        memory.clear(sid);
        remote.clear(sid).catch((error) => onError?.(error));
      },
    };
    return mountRespondentSafe(root, model, {
      mode: detectDevice(root.ownerDocument.defaultView),
      backend: bridge,
      sessionId: id,
      onState: (state) => state,
    });
  }
  return {
    VERSION,
    ParseError,
    parseYaml,
    parseSurvey,
    validateSurvey: validateSurveyComplete,
    compileSurvey,
    condition,
    detectDevice,
    parseProlificLaunch,
    stableSessionId,
    createMemoryBackend,
    createLocalMockBackend: createConcurrentLocalMockBackend,
    createSupabaseBackend: createSecureSupabaseBackend,
    mountRespondent: mountRespondentSafe,
    mountSupabaseRespondent,
  };
});

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
        greedyq: new Set(["spec_version", "version", "organization"]),
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
      page.previous_mode =
        nav.previous_mode ?? (page.show_previous ? "show" : "hide");
      page.next_mode =
        nav.next_mode ?? (nav.show_next === false ? "hide" : "show");
      page.next_delay_seconds = nav.next_delay_seconds ?? 0;
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
      study_version: config.study?.version || "unknown",
      greedyq_version: front.greedyq?.version,
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
        if (!response.ok)
          throw new Error(`Supabase RPC ${name} failed (${response.status}).`);
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
  function resolveProlificLaunch(search, mode = "test") {
    const parsed = parseProlificLaunch(search, mode),
      supplied = Object.values(parsed.identifiers).filter(Boolean);
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
      const selected = state.answers[q.id] ?? q._answer,
        initial = selected ?? q.selected,
        today = new Date().toISOString().slice(0, 10);
      if (q.type === "custom")
        return `<div class="gq-custom ${esc(q.custom_class || "")}" data-customization="${esc(q.customization || "")}">${input({ ...q, type: q.base_type })}</div>`;
      if (q.type === "rank_order")
        return `<div class="gq-rank-order">${(q.options || []).map((o) => `<label><span>${esc(o.label)}</span><select data-rank-item="${esc(o.value)}"><option value="">Rank</option>${q.options.map((_, i) => `<option value="${i + 1}" ${selected?.[o.value] === i + 1 ? "selected" : ""}>${i + 1}</option>`).join("")}</select></label>`).join("")}</div>`;
      if (q.type === "nps") {
        const min = q.min ?? 0, max = q.max ?? 10;
        return `<div class="gq-nps"><div class="gq-nps-scale">${Array.from({ length: max - min + 1 }, (_, i) => min + i).map((n) => `<label><input type="radio" name="${esc(q.id)}" value="${n}" ${selected === n ? "checked" : ""}><span>${n}</span></label>`).join("")}</div><div class="gq-nps-anchors"><span>${esc(q.low_label || "Not at all likely")}</span><span>${esc(q.high_label || "Extremely likely")}</span></div></div>`;
      }
      if (q.type === "timing")
        return `<input type="hidden" data-id="${esc(q.id)}" data-timing value="${Math.max(0, Math.round((Date.now() - (state.page_entered_at || Date.now())) / 1000))}">`;
      if (q.type === "constant_sum") {
        const total = q.total ?? 100;
        return `<div class="gq-constant-sum">${(q.options || []).map((o) => `<label><span>${esc(o.label)}</span><input type="number" min="0" step="${esc(q.step ?? 1)}" data-constant-item="${esc(o.value)}" value="${esc(selected?.[o.value] ?? 0)}"></label>`).join("")}<output data-constant-total>0 / ${esc(total)}</output></div>`;
      }
      if (q.type === "side_by_side")
        return `<div class="gq-side-by-side">${(q.columns || []).map((column) => `<section><h3>${esc(column.label)}</h3>${input({ ...q, id: `${q.id}:${column.value}`, type: "matrix", columns: undefined, mobile_columns: q.mobile_columns ?? 3, _answer: selected?.[column.value] })}</section>`).join("")}</div>`;
      if (q.type === "pick_group_rank")
        return `<div class="gq-pick-group-rank">${(q.options || []).map((o) => `<div class="gq-pgr-item"><strong>${esc(o.label)}</strong><label>Group<select data-pgr-group="${esc(o.value)}"><option value="">Choose</option>${(q.groups || []).map((g) => `<option value="${esc(g.value)}" ${selected?.[o.value]?.group === g.value ? "selected" : ""}>${esc(g.label)}</option>`).join("")}</select></label><label>Rank<input type="number" min="1" max="${q.options.length}" data-pgr-rank="${esc(o.value)}" value="${esc(selected?.[o.value]?.rank ?? "")}"></label></div>`).join("")}</div>`;
      if (q.type === "drill_down") {
        const separator = q.path_separator || " > ", paths = (q.options || []).map((o) => String(o.label).split(separator)), current = Array.isArray(selected) ? selected : [], levels = Math.max(0, ...paths.map((p) => p.length));
        return `<div class="gq-drill-down" data-separator="${esc(separator)}">${Array.from({ length: levels }, (_, level) => { const prefix = current.slice(0, level); const choices = [...new Set(paths.filter((path) => prefix.every((part, i) => path[i] === part)).map((path) => path[level]).filter(Boolean))]; return `<label>Level ${level + 1}<select data-drill-level="${level}"><option value="">Choose</option>${choices.map((choice) => `<option value="${esc(choice)}" ${current[level] === choice ? "selected" : ""}>${esc(choice)}</option>`).join("")}</select></label>`; }).join("")}</div>`;
      }
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
          ? `<details class="gq-transcript"><summary>Transcript</summary><p>${esc(q.transcript)}</p></details>`
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
                          return `<label class="gq-matrix-mobile-cell"><span>${esc(o.label)}</span><input type="${cellType}" aria-label="${esc(`${r.label} — ${o.label}`)}" name="${esc(q.id + ":" + r.value)}" value="${esc(o.value)}" ${checked ? "checked" : ""}></label>`;
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
        return `<div class="gq-date-range"><label>Start<input data-id="${esc(q.id)}" data-date-index="0" type="date" value="${esc(range[0] || "")}"></label><label>End<input data-id="${esc(q.id)}" data-date-index="1" type="date" value="${esc(range[1] || "")}"></label></div>`;
      }
      if (q.type === "textarea")
        return `<textarea data-id="${esc(q.id)}" placeholder="${esc(q.placeholder || "")}" style="${q.height ? `height:${esc(q.height)};` : ""}${q.resize ? `resize:${esc(q.resize)};` : ""}" cols="${esc(q.cols || 80)}">${esc(selected || "")}</textarea>`;
      return `<input data-id="${esc(q.id)}" type="${q.type === "numeric" ? "number" : q.type === "date" ? "date" : "text"}" placeholder="${esc(q.placeholder || "")}" value="${esc(selected ?? q.selected ?? (q.type === "date" ? today : ""))}" ${q.min != null ? `min="${q.min}"` : ""} ${q.max != null ? `max="${q.max}"` : ""}>`;
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
      const v = state.answers[q.id];
      if (q.type === "rank_order" && v) {
        const ranks = Object.values(v);
        if (new Set(ranks).size !== ranks.length) return "Use each rank only once.";
        if (q.required && ranks.length !== (q.options || []).length) return "Rank every item.";
      }
      if (q.type === "constant_sum" && v && Object.values(v).reduce((a, b) => a + Number(b || 0), 0) !== (q.total ?? 100))
        return `The allocation must total ${q.total ?? 100}.`;
      if (q.type === "side_by_side" && q.required && (q.columns || []).some((column) => (q.rows || []).some((row) => !Object.hasOwn(v?.[column.value] || {}, row.value))))
        return "Answer every row in every column.";
      if (q.type === "pick_group_rank" && v) {
        if (q.required && Object.keys(v).length !== (q.options || []).length) return "Place every item in a group.";
        for (const group of q.groups || []) { const ranks = Object.values(v).filter((item) => item.group === group.value).map((item) => item.rank).filter(Boolean); if (new Set(ranks).size !== ranks.length) return `Use each rank only once within ${group.label}.`; }
      }
      if (q.type === "drill_down" && q.required) {
        const separator = q.path_separator || " > ", valid = (q.options || []).some((option) => String(option.label).split(separator).join("\u0000") === (v || []).join("\u0000"));
        if (!valid) return "Complete every level of the selection.";
      }
      return null;
    }
    function save() {
      backend.save(sessionId, state);
      options.onState?.(JSON.parse(JSON.stringify(state)));
    }
    let renderedPage = null;
    let delayTimer = null;
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
      card.innerHTML = `<p class="gq-eyebrow">${esc(model.title)}</p><h1>${esc(p.title)}</h1><div class="gq-copy">${esc(p.body || "")}</div>${visible(
        p,
      )
        .map(
          (q) =>
            `<fieldset class="gq-q gq-${esc(q.type)} gq-direction-${esc(q.direction || "horizontal")}${q.justified ? " gq-justified" : ""}" data-q="${esc(q.id)}" style="${q.width ? `width:${esc(q.width)}` : ""}"><legend>${esc(q.label)}${q.required ? ' <span aria-label="required">*</span>' : ""}</legend>${input(q)}</fieldset>`,
        )
        .join(
          "",
        )}${message ? `<p class="gq-error" role="alert">${esc(message)}</p>` : ""}<div class="gq-actions">${showBack ? `<button data-back ${backDisabled ? "disabled" : ""}>${esc(model.messages.previous)}</button>` : ""}${p.terminal ? `<strong>${esc(p.terminal)}</strong>` : showNext ? `<button data-next ${nextDisabled ? "disabled" : ""}>${esc(p.next_label || model.messages.next)}${delayRemaining > 0 ? ` (${Math.ceil(delayRemaining / 1000)}s)` : ""}</button>` : ""}</div>`;
      if (delayRemaining > 0 && nextMode !== "disable")
        delayTimer = setTimeout(() => render(message), Math.min(1000, delayRemaining));
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
      for (const sum of card.querySelectorAll(".gq-constant-sum")) {
        const updateSum = () => { const values = [...sum.querySelectorAll("[data-constant-item]")].map((e) => Number(e.value || 0)); const qid = sum.closest("[data-q]")?.dataset.q, question = (p.questions || []).find((item) => item.id === qid), total = question?.total ?? 100; sum.querySelector("[data-constant-total]").textContent = `${values.reduce((a, b) => a + b, 0)} / ${total}`; };
        sum.addEventListener("input", updateSum); updateSum();
      }
      for (const drill of card.querySelectorAll(".gq-drill-down select"))
        drill.addEventListener("change", () => { collect(p); save(); render(); });
      const visibilitySources = new Set(
        (p.questions || [])
          .map((question) => question.show_if?.field)
          .filter(Boolean),
      );
      for (const control of card.querySelectorAll("input,select,textarea"))
        control.addEventListener("change", () => {
          const source = control.name?.split(":")[0] || control.dataset.id;
          if (!visibilitySources.has(source)) return;
          collect(p);
          save();
          render();
        });
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
          const invalidAnswer = visible(p).map((q) => [q, answerProblem(q)]).find(([, problem]) => problem);
          if (invalidAnswer) { render(invalidAnswer[1]); card.querySelector(`[data-q="${CSS.escape(invalidAnswer[0].id)}"] input,[data-q="${CSS.escape(invalidAnswer[0].id)}"] select`)?.focus(); return; }
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
    { url, anonKey, sessionId, externalIdentifiers, onError } = {},
  ) {
    const storageKey = `greedyq-capability:${model.study_id}:${externalIdentifiers?.SESSION_ID || "direct"}`,
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
      studyVersion: model.study_version,
      greedyqVersion: model.greedyq_version,
      specVersion: "0.2",
      isTest: model.runtime_policy?.mode !== "production",
      consentQuestion: model.runtime_policy?.consent?.question,
    });
    await remote.create(id);
    if (externalIdentifiers)
      await remote.registerExternal(id, externalIdentifiers);
    const loaded = await remote.load(id),
      memory = createMemoryBackend();
    if (loaded?.state && typeof loaded.state.page === "string")
      memory.save(id, {
        ...loaded.state,
        condition: loaded.condition ?? loaded.state.condition ?? null,
      });
    else if (typeof loaded?.page === "string") memory.save(id, loaded);
    let initialCondition =
      loaded?.condition ?? loaded?.state?.condition ?? null;
    if (!model.assignment_page && !initialCondition)
      initialCondition = await remote.assign(
        id,
        model.conditions || ["default"],
      );
    const bridge = {
      kind: "supabase-bridge",
      load: memory.load,
      assign: (sid, conditions) =>
        initialCondition || remote.assign(sid, conditions),
      inspect: memory.inspect,
      save: (sid, state) => {
        memory.save(sid, state);
        const persistedState = {
          ...state,
          lifecycle:
            state.lifecycle === "active"
              ? state.consent_accepted
                ? "in_progress"
                : "created"
              : state.lifecycle,
        };
        remote.save(sid, persistedState).catch((error) => onError?.(error));
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
    resolveProlificLaunch,
    stableSessionId,
    createMemoryBackend,
    createLocalMockBackend: createConcurrentLocalMockBackend,
    createSupabaseBackend: createSecureSupabaseBackend,
    mountRespondent: mountRespondentSafe,
    mountSupabaseRespondent,
  };
});

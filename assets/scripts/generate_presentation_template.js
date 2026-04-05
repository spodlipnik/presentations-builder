/**
 * PptxGenJS presentation generator.
 *
 * Reads:
 *   - theme.yaml: tokens + roles.variants specs
 *   - slides.json: per-slide {slide_number, type, variant, content, image, speaker}
 *
 * Writes:
 *   - presentation.pptx in project root
 *
 * Usage:
 *   NODE_PATH=${CLAUDE_PLUGIN_DATA}/node_modules node generate_presentation.js
 */
const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");
const pptxgen = require("pptxgenjs");

// ===== Configuration (written by talk-slides skill) =====
const THEME_PATH = "${THEME_PATH}";
const SLIDES_JSON_PATH = "${SLIDES_JSON_PATH}";
const IMAGES_DIR = "${IMAGES_DIR}";
const OUTPUT_PATH = "${OUTPUT_PATH}";
// =========================================================

function loadTheme(themePath) {
    const raw = fs.readFileSync(themePath, "utf8");
    return yaml.load(raw).theme;
}

function loadSlides(jsonPath) {
    return JSON.parse(fs.readFileSync(jsonPath, "utf8"));
}

function resolveColor(tokenOrHex, tokens) {
    // "text" → tokens.color.text, "#FF0000" → "FF0000" (strip #)
    if (typeof tokenOrHex !== "string") return "000000";
    if (tokenOrHex.startsWith("#")) return tokenOrHex.slice(1).toUpperCase();
    if (tokens.color && tokens.color[tokenOrHex]) {
        return tokens.color[tokenOrHex].replace(/^#/, "").toUpperCase();
    }
    return "000000";  // fallback
}

function resolveFont(slotFont, tokens) {
    // slot may have family, size, weight, color, align
    // defaults from tokens.typography.heading if nothing specified
    const headingDefaults = tokens.typography.heading || {};
    const bodyDefaults = tokens.typography.body || {};
    return {
        fontFace: slotFont.family || bodyDefaults.family || "Arial",
        fontSize: slotFont.size || bodyDefaults.size_pt || 18,
        bold: slotFont.weight === "bold" || slotFont.weight === 700,
        color: resolveColor(slotFont.color || "text", tokens),
        align: slotFont.align || "left",
    };
}

function findVariant(theme, roleId, variantId) {
    const role = (theme.roles || {})[roleId];
    if (!role) return null;
    const variant = (role.variants || []).find(v => v.id === variantId);
    return variant || (role.variants || [])[0] || null;
}

function renderSlide(pres, theme, slideData, imagesDir) {
    const variant = findVariant(theme, slideData.type, slideData.variant);
    if (!variant) {
        console.warn(`No variant found for slide ${slideData.slide_number}: type=${slideData.type}, variant=${slideData.variant}`);
        const pptxSlide = pres.addSlide();
        pptxSlide.addText(`[missing layout: ${slideData.type}/${slideData.variant}]`, {
            x: 0.5, y: 0.5, w: 9, h: 1, fontSize: 20, color: "FF0000",
        });
        return;
    }

    const pptxSlide = pres.addSlide();
    const slideW = theme.tokens.slide.width_in;
    const slideH = theme.tokens.slide.height_in;
    const tokens = theme.tokens;

    // Render each slot in the variant's layout
    const layout = variant.layout || {};
    for (const [slotName, slotDef] of Object.entries(layout)) {
        const [x, y, w, h] = slotDef.box;  // fractions

        if (slotName === "image" || slotDef.kind === "image_or_chart" || slotDef.fit) {
            // Image slot
            if (slideData.image) {
                const imagePath = path.join(imagesDir, slideData.image);
                if (fs.existsSync(imagePath)) {
                    pptxSlide.addImage({
                        path: imagePath,
                        x: x * slideW, y: y * slideH,
                        w: w * slideW, h: h * slideH,
                        sizing: slotDef.fit === "cover"
                            ? { type: "cover", w: w * slideW, h: h * slideH }
                            : { type: "contain", w: w * slideW, h: h * slideH },
                    });
                }
            }
        } else {
            // Text slot — use content for main text slots
            const text = _slotText(slotName, slideData);
            if (!text) continue;
            const font = resolveFont(slotDef.font || {}, tokens);
            pptxSlide.addText(text, {
                x: x * slideW, y: y * slideH,
                w: w * slideW, h: h * slideH,
                fontFace: font.fontFace,
                fontSize: font.fontSize,
                bold: font.bold,
                color: font.color,
                align: font.align,
                margin: 0,
                valign: "top",
            });
        }
    }
}

function _slotText(slotName, slideData) {
    // Map slot names → slide data fields
    const name = slotName.toLowerCase();
    if (name === "title" || name === "headline" || name === "message") {
        // Use content or first line of content
        const content = slideData.content || "";
        return content.split("\n")[0];
    }
    if (name === "subtitle" || name === "caption" || name === "body" || name === "evidence") {
        const lines = (slideData.content || "").split("\n");
        return lines.slice(1).join("\n") || "";
    }
    if (name === "author" || name === "affiliation" || name === "date") {
        // These come from talk.yaml metadata — handled by caller
        return "";
    }
    return slideData.content || "";
}

// ===== Main =====
const theme = loadTheme(THEME_PATH);
const slides = loadSlides(SLIDES_JSON_PATH);

const pres = new pptxgen();
pres.layout = theme.tokens.aspect_ratio === "16:9" ? "LAYOUT_16x9" : "LAYOUT_4x3";

// Default slide master for theme tokens
pres.defineSlideMaster({
    title: "THEME_MASTER",
    background: { color: resolveColor(theme.tokens.color.background || "FFFFFF", theme.tokens) },
});

for (const slide of slides) {
    renderSlide(pres, theme, slide, IMAGES_DIR);
}

pres.writeFile({ fileName: OUTPUT_PATH })
    .then(() => console.log(`Generated: ${OUTPUT_PATH}`))
    .catch(err => {
        console.error("Generation failed:", err);
        process.exit(1);
    });

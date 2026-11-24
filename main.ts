// Post the Meme, Win the Feed — make.fun entry
//
// The entry is an X post: the meme picture (meme.png, made in this session)
// is posted from the entrant's public X account with @_myronera tagged and
// the account's make.fun play code in the post text, and the post's address
// goes in POST.json at this repository's root.
//
// All this program has to do is copy POST.json from the repository to the
// output directory, byte for byte. The house reads the post itself from X
// and writes its counts to /output/post.counts.json afterwards; nothing this
// program writes about the post counts.
//
// No network, no wall clock, no files outside the repository: the two runs
// of this entry write the same bytes.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";

const botDir = resolve(process.env.MAKEFUN_BOT_DIR ?? process.cwd());
const outputDir = resolve(
  process.env.MAKEFUN_OUTPUT_DIR ?? process.env.OUTPUT_DIR ?? "/output",
);

const source = join(botDir, "POST.json");
let raw: string;
try {
  raw = readFileSync(source, "utf8");
} catch {
  throw new Error(`cannot read ${source}: post the meme on X first, then fill in POST.json`);
}
const parsed: unknown = JSON.parse(raw);
const url =
  typeof parsed === "object" && parsed !== null
    ? (parsed as { url?: unknown }).url
    : undefined;
if (typeof url !== "string" || url.length === 0) {
  throw new Error("POST.json must be a JSON object with a non-empty string \"url\"");
}
try {
  new URL(url);
} catch {
  throw new Error(`POST.json "url" is not an absolute URL: ${url}`);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, join(outputDir, "POST.json"));

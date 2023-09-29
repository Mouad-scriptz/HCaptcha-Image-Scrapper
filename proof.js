// https://github.com/xtekky/Discord-Hcaptcha-Solver

const fs      = require('fs')
const { JSDOM, ResourceLoader } = require("jsdom");

const hsw     = fs.readFileSync(__dirname + "/hsw.js", "utf-8");
let userAgent = process.argv[3]

const {window}  = new JSDOM(``, {
    url                 : "https://discord.com",
    referrer            : "https://discord.com",
    contentType         : "text/html",
    includeNodeLocations: false,
    runScripts          : "outside-only",
    pretendToBeVisual   : true,
    resources           : new ResourceLoader({ userAgent })
});

_window_ = window;
_window_.eval(hsw)

token = process.argv[2]

_window_.get_hsw(token).then(function (result) {
    console.log(result)
})


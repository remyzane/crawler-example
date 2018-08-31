treat = require 'treat'

function main(splash, args)

    splash:autoload([[
function test() {
    console.log('in test')
}
    ]])

    local output = {}

end
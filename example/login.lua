treat = require 'treat'
json = require 'json'
base64 = require 'base64'

function main(splash, args)

    local output = {}
    local image_name
    local image_base64
    local slide_block_x_value
    splash.response_body_enabled = true

    splash:on_response(function(response)
        local url = tostring(response.request.url)
        -- table.insert(output, url)

        if string.find(url, '_bg.jpg') and response.ok then
            image_name = url:gmatch("[^/]*$")()
            image_base64 = response.info.content.text
            -- table.insert(output, response.info.content)
            -- table.insert(output, response.headers)
        end

        if string.find(url, args.api) then  -- args.api 中不能有通配符 ? 否则无法 find
            local result = json.decode(treat.as_string(response.body))
            if result.code == 'ok' then
                slide_block_x_value = result.value
            end
        end

    end)

    assert(splash:go(args.url))
    splash:wait(args.load_time)

    if image_name then
        table.insert(output, image_name)
        body = '--'..args.boundary..'\r\nContent-Disposition: form-data; name="file"; '
        body = body..'filename="'..image_name..'"\r\n\r\n'
        body = body..image_base64
        body = body..'\r\n--'..args.boundary..'--\r\n'

        assert(splash:http_post{args.api..'?file_format=base64', headers={
            ['Content-Length'] = string.len(body),
            ['Content-Type'] = 'multipart/form-data; boundary='..args.boundary,
        }, body=body})
        splash:wait(0.5)
    end

    if slide_block_x_value then
        table.insert(output, slide_block_x_value)
    end

    return treat.as_array(output)

end


--    splash:go{url="%s", headers={
--        ["Cookie"] = "session=.eJwlzkFqBDEMRNG7eJ0G2bIlqy8zuK0rXml29",
--    }}
--
--    local title = splash:evaljs("document.title")
--
--   splash:set_custom_headers({
--       ["Header-1"] = "Value 1",
--       ["Header-2"] = "Value 2",
--    })
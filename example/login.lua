treat = require 'treat'
json = require 'json'
base64 = require 'base64'

function main(splash, args)

    local output = {}
    local image_name
    local image_base64
    local slide_block_x_value
    splash.response_body_enabled = true

--    assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))

--      local get_dt = splash:jsfunc('get_document_title')
--      return get_dt()..'bbb'
--  return splash:evaljs("get_document_title()")

    splash:on_response(function(response)
        local url = tostring(response.request.url)
        -- table.insert(output, url)

        if string.find(url, '_bg.jpg') and response.ok then
            image_name = url:gmatch("[^/]*$")()
            image_base64 = response.info.content.text
            -- table.insert(output, response.info.content)
            -- table.insert(output, response.headers)
        end

        -- string.find 的第二个参数（正则表达式）不能写成 args.api，应为 args.api中有字符?（通配符）
        if string.find(url, 'recognize_x_coordinate') then
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

        assert(splash:http_post{args.api, headers={
            ['Content-Length'] = string.len(body),
            ['Content-Type'] = 'multipart/form-data; boundary='..args.boundary,
        }, body=body})
        splash:wait(0.5)
    end

    if slide_block_x_value then
        table.insert(output, slide_block_x_value)

        local element = splash:select('.shumei_captcha_slide_btn')
        local bounds = element:bounds()
        local elm_x = bounds.left + bounds.width/2
        local elm_y = bounds.top + bounds.height/2

        splash:mouse_press{  y=elm_y+math.random(-5,5), x=elm_x+math.random(-5,5)}
        splash:mouse_release{y=elm_y+math.random(-5,5), x=elm_x+math.random(-5,5)+50 }
        splash:wait(1)
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
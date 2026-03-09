package com.jsl26tp.jsl26tp.home.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

    @Value("${kakao.js-key}")
    private String kakaoJsKey;

    // 메인 페이지 (지도)
    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("kakaoJsKey", kakaoJsKey);
        return "index";
    }
}

package com.jsl26tp.jsl26tp.home.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class HomeController {

    @Value("${naver.maps.client-id}")
    private String naverMapsClientId;

    // 메인 페이지 (지도)
    @GetMapping("/")
    public String home(@RequestParam(required = false) Long id, Model model) {
        model.addAttribute("naverMapsClientId", naverMapsClientId);
        model.addAttribute("targetId", id);
        return "index";
    }

    // 프라이버시 정책 페이지
    @GetMapping("/privacy")
    public String privacy() {
        return "privacy";
    }

    // 이용약관 페이지
    @GetMapping("/terms")
    public String terms() {
        return "terms";
    }

}

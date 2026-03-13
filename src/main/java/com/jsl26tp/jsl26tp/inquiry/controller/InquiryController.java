package com.jsl26tp.jsl26tp.inquiry.controller;

import com.jsl26tp.jsl26tp.auth.domain.User;
import com.jsl26tp.jsl26tp.auth.service.UserService;
import com.jsl26tp.jsl26tp.config.CustomUserDetails;
import com.jsl26tp.jsl26tp.inquiry.domain.Inquiry;
import com.jsl26tp.jsl26tp.inquiry.service.InquiryService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequiredArgsConstructor
public class InquiryController {

    private final InquiryService inquiryService;
    private final UserService userService;

    // 문의하기 폼 (GET /inquiry)
    @GetMapping("/inquiry")
    public String inquiryForm(@AuthenticationPrincipal CustomUserDetails userDetails, Model model) {
        // 내 문의 내역도 함께 표시
        User user = userService.findByUsername(userDetails.getUsername());
        model.addAttribute("inquiries", inquiryService.findByWriterId(user.getId()));
        return "inquiry/index";
    }

    // 문의 제출 (POST /inquiry)
    @PostMapping("/inquiry")
    public String submitInquiry(@AuthenticationPrincipal CustomUserDetails userDetails,
                                @RequestParam String title,
                                @RequestParam String content) {
        User user = userService.findByUsername(userDetails.getUsername());
        Inquiry inquiry = new Inquiry();
        inquiry.setWriterId(user.getId());
        inquiry.setTitle(title);
        inquiry.setContent(content);
        inquiryService.insertInquiry(inquiry);
        return "redirect:/inquiry?success=true";
    }
}

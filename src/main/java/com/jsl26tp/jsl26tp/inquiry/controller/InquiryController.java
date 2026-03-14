package com.jsl26tp.jsl26tp.inquiry.controller;

import com.jsl26tp.jsl26tp.common.ApiResponse;
import com.jsl26tp.jsl26tp.config.CustomUserDetails;
import com.jsl26tp.jsl26tp.inquiry.domain.Inquiry;
import com.jsl26tp.jsl26tp.inquiry.service.InquiryService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class InquiryController {

    private final InquiryService inquiryService;

    // Inquiry page - GET /inquiry
    @GetMapping("/inquiry")
    public String inquiryPage(@AuthenticationPrincipal CustomUserDetails user, Model model) {
        List<Inquiry> inquiries = inquiryService.findByWriterId(user.getId());
        model.addAttribute("inquiries", inquiries);
        return "inquiry/index";
    }

    // Submit inquiry form - POST /inquiry
    @PostMapping("/inquiry")
    public String submitInquiry(@RequestParam String title,
                                @RequestParam String content,
                                @AuthenticationPrincipal CustomUserDetails user) {
        Inquiry inquiry = new Inquiry();
        inquiry.setTitle(title);
        inquiry.setContent(content);
        inquiry.setWriterId(user.getId());
        inquiryService.createInquiry(inquiry);
        return "redirect:/inquiry?success";
    }

    // ===== API endpoints =====

    @PostMapping("/api/inquiries")
    @ResponseBody
    public ApiResponse<Void> createInquiry(
            @RequestBody Inquiry inquiry,
            @AuthenticationPrincipal CustomUserDetails user) {
        inquiry.setWriterId(user.getId());
        inquiryService.createInquiry(inquiry);
        return ApiResponse.ok();
    }

    @GetMapping("/api/inquiries/my")
    @ResponseBody
    public ApiResponse<List<Inquiry>> getMyInquiries(
            @AuthenticationPrincipal CustomUserDetails user) {
        List<Inquiry> inquiries = inquiryService.findByWriterId(user.getId());
        return ApiResponse.ok(inquiries);
    }

    @GetMapping("/api/inquiries/{id}")
    @ResponseBody
    public ApiResponse<Inquiry> getInquiryDetail(@PathVariable Long id) {
        Inquiry inquiry = inquiryService.getInquiryDetail(id);
        return ApiResponse.ok(inquiry);
    }

    @DeleteMapping("/api/inquiries/{id}")
    @ResponseBody
    public ApiResponse<Void> deleteInquiry(
            @PathVariable Long id,
            @AuthenticationPrincipal CustomUserDetails user) {
        inquiryService.deleteInquiry(id, user.getId());
        return ApiResponse.ok();
    }
}

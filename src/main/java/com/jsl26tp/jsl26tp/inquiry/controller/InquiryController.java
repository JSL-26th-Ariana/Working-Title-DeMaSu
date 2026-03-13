package com.jsl26tp.jsl26tp.inquiry.controller;

import com.jsl26tp.jsl26tp.common.ApiResponse;
import com.jsl26tp.jsl26tp.config.CustomUserDetails;
import com.jsl26tp.jsl26tp.inquiry.domain.Inquiry;
import com.jsl26tp.jsl26tp.inquiry.service.InquiryService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * お問い合わせ Controller (ユーザー向け)
 *
 * 유저가 문의를 등록/조회/삭제하는 API
 * - 관리자 문의 처리(답변 등)는 AdminController에서 담당
 * - 모든 엔드포인트 로그인 필요 (SecurityConfig → anyRequest().authenticated())
 */
@RestController
@RequestMapping("/api/inquiries")
@RequiredArgsConstructor
public class InquiryController {

    private final InquiryService inquiryService;

    /**
     * 문의 등록
     * POST /api/inquiries
     *
     * @param inquiry { title: "제목", content: "내용" }
     * @param user    로그인 유저 (writerId 자동 세팅)
     */
    @PostMapping
    public ApiResponse<Void> createInquiry(
            @RequestBody Inquiry inquiry,
            @AuthenticationPrincipal CustomUserDetails user) {

        inquiry.setWriterId(user.getId());
        inquiryService.createInquiry(inquiry);
        return ApiResponse.ok();
    }

    /**
     * 내 문의 목록 조회
     * GET /api/inquiries/my
     */
    @GetMapping("/my")
    public ApiResponse<List<Inquiry>> getMyInquiries(
            @AuthenticationPrincipal CustomUserDetails user) {

        List<Inquiry> inquiries = inquiryService.findByWriterId(user.getId());
        return ApiResponse.ok(inquiries);
    }

    /**
     * 문의 상세 조회
     * GET /api/inquiries/{id}
     */
    @GetMapping("/{id}")
    public ApiResponse<Inquiry> getInquiryDetail(@PathVariable Long id) {

        Inquiry inquiry = inquiryService.getInquiryDetail(id);
        return ApiResponse.ok(inquiry);
    }

    /**
     * 문의 삭제 (소프트 삭제, 본인만)
     * DELETE /api/inquiries/{id}
     */
    @DeleteMapping("/{id}")
    public ApiResponse<Void> deleteInquiry(
            @PathVariable Long id,
            @AuthenticationPrincipal CustomUserDetails user) {

        inquiryService.deleteInquiry(id, user.getId());
        return ApiResponse.ok();
    }
}

package com.jsl26tp.jsl26tp.auth.controller;

import com.jsl26tp.jsl26tp.auth.domain.User;
import com.jsl26tp.jsl26tp.auth.service.UserService;
import com.jsl26tp.jsl26tp.common.ApiResponse;
import com.jsl26tp.jsl26tp.inquiry.service.InquiryService;
import com.jsl26tp.jsl26tp.review.service.ReviewService;
import com.jsl26tp.jsl26tp.toilet.service.RecentViewService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import com.jsl26tp.jsl26tp.common.BusinessException;

@Controller
@RequestMapping("/mypage")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;
    private final RecentViewService recentViewService;
    private final ReviewService reviewService;
    private final InquiryService inquiryService;

    // 1. 마이페이지 메인 (GET /mypage)
    @GetMapping
    public String index(@AuthenticationPrincipal UserDetails userDetails, Model model) {
        // Security에서 가져온 username으로 유저 정보 조회
        User user = userService.findByUsername(userDetails.getUsername());
        model.addAttribute("user", user);
        return "mypage/index"; // templates/mypage/index.html
    }

    // 2. 프로필 수정 처리 (POST /mypage/edit)
    @PostMapping("/edit")
    public String updateProfile(@AuthenticationPrincipal UserDetails userDetails,
                                User updateData,
                                @RequestParam(value = "iconFile", required = false) MultipartFile profileImage,
                                Model model) {
        User user = userService.findByUsername(userDetails.getUsername());
        updateData.setId(user.getId());

        // 프리셋 아이콘 선택 확인 (hidden input에서 전달)
        if (updateData.getIconUrl() != null && updateData.getIconUrl().startsWith("/images/profiles/")) {
            // 프리셋 아이콘 선택됨 → 그대로 사용
        } else {
            // 기존 방식: 파일 업로드 처리
            String imageUrl = userService.saveProfileImage(profileImage);
            if (imageUrl != null) {
                updateData.setIconUrl(imageUrl);
            } else {
                updateData.setIconUrl(user.getIconUrl());
            }
        }

        try {
            userService.updateUser(updateData);
        } catch (BusinessException e) {
            model.addAttribute("user", updateData);
            model.addAttribute("errorMessage", e.getErrorCode().getMessage());
            return "mypage/edit"; // 에러 시 폼으로 다시 돌아감
        }

        return "redirect:/mypage";
    }

    // 2-1. 프로필 수정 폼 (GET /mypage/edit)
    @GetMapping("/edit")
    public String editForm(@AuthenticationPrincipal UserDetails userDetails, Model model) {
        User user = userService.findByUsername(userDetails.getUsername());
        model.addAttribute("user", user);
        return "mypage/edit";
    }

    // 3. 비밀번호 변경 폼 (GET /mypage/password)
    @GetMapping("/password")
    public String passwordForm(@AuthenticationPrincipal UserDetails userDetails, Model model) {
        User user = userService.findByUsername(userDetails.getUsername());
        model.addAttribute("user", user); // ← 추가
        return "mypage/password";
    }

    // 4. 비밀번호 변경 처리 (POST /mypage/password)
    @PostMapping("/password")
    @ResponseBody
    public ApiResponse<Void> updatePassword(@AuthenticationPrincipal UserDetails userDetails,
                                            @RequestParam String currentPassword,
                                            @RequestParam String newPassword) {
        User user = userService.findByUsername(userDetails.getUsername());
        userService.updatePassword(user.getId(), currentPassword, newPassword);
        return ApiResponse.ok(null);
    }

    // 5. 최근 본 화장실 (GET /mypage/recent)
    @GetMapping("/recent")
    public String recent(@AuthenticationPrincipal UserDetails userDetails, Model model) {
        // 1. 현재 로그인한 유저 정보 가져오기
        User user = userService.findByUsername(userDetails.getUsername());

        // 2. 유저 ID로 최근 본 화장실 목록 조회해서 모델에 담기
        model.addAttribute("recentToilets", recentViewService.findByUserId(user.getId()));

        return "mypage/recent"; // templates/mypage/recent.html
    }

    // 6. 내가 쓴 리뷰 (GET /mypage/reviews)
    @GetMapping("/reviews")
    public String myReviews(@AuthenticationPrincipal UserDetails userDetails, Model model) {
        User user = userService.findByUsername(userDetails.getUsername());
        model.addAttribute("user", user); // ← 추가
        model.addAttribute("reviews", reviewService.getMyReviews(user.getId()));
        return "mypage/reviews";
    }

    // 7. 내 문의 내역 (GET /mypage/inquiries)
    @GetMapping("/inquiries")
    public String myInquiries(@AuthenticationPrincipal UserDetails userDetails, Model model) {
        User user = userService.findByUsername(userDetails.getUsername());
        model.addAttribute("user", user);
        model.addAttribute("inquiries", inquiryService.findByWriterId(user.getId()));
        return "mypage/inquiries";
    }

    // 8. 프로필 아이콘 선택 (POST /mypage/api/icon)
    @PostMapping("/api/icon")
    @ResponseBody
    public ApiResponse<String> updateProfileIcon(@AuthenticationPrincipal UserDetails userDetails,
                                                  @RequestParam String iconName) {
        User user = userService.findByUsername(userDetails.getUsername());
        userService.updateProfileIcon(user.getId(), iconName);
        return ApiResponse.ok("OK");
    }

    // 9. 최근 본 화장실 개별 삭제 (DELETE /mypage/recent/{toiletId})
    @DeleteMapping("/recent/{toiletId}")
    @ResponseBody
    public ApiResponse<Void> deleteRecentView(@AuthenticationPrincipal UserDetails userDetails,
                                              @PathVariable Long toiletId) {
        User user = userService.findByUsername(userDetails.getUsername());
        recentViewService.deleteByToiletId(user.getId(), toiletId);
        return ApiResponse.ok(null);
    }

    // 10. 최근 본 화장실 전체 삭제 (DELETE /mypage/recent)
    @DeleteMapping("/recent")
    @ResponseBody
    public ApiResponse<Void> deleteAllRecentViews(@AuthenticationPrincipal UserDetails userDetails) {
        User user = userService.findByUsername(userDetails.getUsername());
        recentViewService.deleteByUserId(user.getId());
        return ApiResponse.ok(null);
    }
}
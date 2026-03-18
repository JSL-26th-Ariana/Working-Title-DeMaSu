package com.jsl26tp.jsl26tp.auth.controller;

import com.jsl26tp.jsl26tp.auth.service.UserService;
import com.jsl26tp.jsl26tp.common.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

/**
 * 비밀번호 찾기(재설정) API — 비로그인 사용자도 접근 가능한 공개 엔드포인트
 * SecurityConfig에서 permitAll() 처리됨
 */
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class PasswordResetController {

    private final UserService userService;

    /**
     * 1단계: 본인 확인
     * POST /api/users/verify-identity?username=...&email=...
     * - DB에서 username + email이 일치하는 계정이 있는지 검증
     * - 일치하면 200 OK, 불일치하면 BusinessException → 400
     */
    @PostMapping("/verify-identity")
    public ApiResponse<Void> verifyIdentity(
            @RequestParam String username,
            @RequestParam String email) {
        userService.verifyIdentity(username, email);
        return ApiResponse.ok(null);
    }

    /**
     * 2단계: 새 비밀번호로 변경
     * POST /api/users/reset-password?username=...&email=...&newPassword=...
     * - 본인 확인 후 새 비밀번호로 업데이트
     * - 8자 미만이면 INVALID_PASSWORD 예외
     */
    @PostMapping("/reset-password")
    public ApiResponse<Void> resetPassword(
            @RequestParam String username,
            @RequestParam String email,
            @RequestParam String newPassword) {
        userService.resetPasswordByIdentity(username, email, newPassword);
        return ApiResponse.ok(null);
    }
}

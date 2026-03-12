package com.jsl26tp.jsl26tp.inquiry.service;

import com.jsl26tp.jsl26tp.inquiry.domain.Inquiry;
import com.jsl26tp.jsl26tp.inquiry.mapper.InquiryMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@RequiredArgsConstructor
public class InquiryService {

    private final InquiryMapper inquiryMapper;

    // 내 문의 내역 조회
    public List<Inquiry> findByWriterId(Long userId) {
        return inquiryMapper.findByWriterId(userId);
    }

    // 문의 등록
    public void insertInquiry(Inquiry inquiry) {
        inquiryMapper.insertInquiry(inquiry);
    }
}
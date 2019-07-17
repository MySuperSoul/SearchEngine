package com.techhub.main.exception;

import com.techhub.main.entity.ResponseData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import javax.validation.ConstraintViolationException;

/**
 * @author ：Chen Xin
 * @date ：Created in 2019/7/17 09:40
 * @modified By：
 */
@RestControllerAdvice
public class ArgumentNotValidException {
    private static Logger log = LoggerFactory.getLogger(ArgumentNotValidException.class);

    @ExceptionHandler(ConstraintViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ResponseData bindException(ConstraintViolationException e) {
        log.info("发生错误");
        log.info(e.getMessage());

        ResponseData responseData = ResponseData.badRequest();
        responseData.putDataValue("error", e.getMessage());
        return responseData;
    }
}
